use gta_all
declare @c int
select @c=count(*) from sys.tables where name='L1_TRDMIN01_ALL'
if(@c=0)
begin
  print '历史数据库总表不存在，开始创建'
  CREATE TABLE [dbo].[L1_TRDMIN01_ALL] (
    [SECCODE] nvarchar(6) COLLATE Chinese_PRC_CI_AS NOT NULL,
    [SECNAME] nvarchar(20) COLLATE Chinese_PRC_CI_AS NOT NULL,
    [TDATE] nvarchar(10) COLLATE Chinese_PRC_CI_AS NOT NULL,
    [MINTIME] nvarchar(4) COLLATE Chinese_PRC_CI_AS NOT NULL,
    [STARTPRC] decimal(9,3) NULL,
    [HIGHPRC] decimal(9,3) NULL,
    [LOWPRC] decimal(9,3) NULL,
    [ENDPRC] decimal(9,3) NULL,
    [MINTQ] decimal(12,0) NULL,
    [MINTM] decimal(18,3) NULL,
    [MARKET] nvarchar(4) COLLATE Chinese_PRC_CI_AS NULL
  )
  print '总表创建成功'
end
else
  print '历史数据总表已经存在'

if object_id('dbo.db_status') is null
begin
  print '临时表db_status 不存在，开始创建'
  create table db_status(
    id int identity(1,1) not null,
    name varchar(40) primary key not null,
    imported int default 0 --0代表尚未导入，1代表已经导入
  )
  print '表db_status 创建成功'
end
else
  print '临时表 db_status 已经存在'

--列出所有的历史数据库，并将其名称插入到临时表中
declare cur cursor for select name from sys.databases
where name like 'GTA_S%'

declare @temp_name varchar(30)
open cur
fetch next from cur into @temp_name
while(@@fetch_status=0)
begin
  if not exists(select name from db_status where name=@temp_name)
  begin
    print '新数据库' + @temp_name + '插入到db_status表中'
    insert into db_status (name) values(@temp_name)
  end
  fetch next from cur into @temp_name
end
close cur
deallocate cur

--列出所有未被导入总库的数据库个数
declare @not_imported_count int
select @not_imported_count=count(*) from db_status where imported=0
print '尚未导入的数据库个数为 : ' + cast(@not_imported_count as varchar)


--循环导入
if @not_imported_count>0
begin
  print '开始循环导入数据到历史数据库'
  declare @i int
  set @i=1
  declare @insert_sql varchar(200)
  declare @final_sql varchar(200)
  declare @db_name varchar(50)
  declare @tb_name varchar(30)
  declare @is_imported int
  declare @db_amount int
  declare @market_str varchar(10)
  select @db_amount=count(*) from db_status
  --开始循环
  while(@i <= @db_amount)
  begin
    select @is_imported = imported from db_status where id=@i
    if(@is_imported=1)
    begin
      set @i=@i+1
      continue
    end
    select @db_name = name from db_status where id=@i
    set @insert_sql='declare tb_cur cursor for select name from '+@db_name+'.sys.tables where name like ''%min01%'''
    exec(@insert_sql)
    set @insert_sql='select SecCode,SecName,tdate,MinTime,StartPrc,HighPrc,LowPrc,EndPrc,MinTq,MinTm,'
    --之前已经声明了tb_cur
    open tb_cur
    fetch next from tb_cur into @tb_name
    while(@@fetch_status=0)
    begin
      print '正在导入' + @db_name + '.dbo.' + @tb_name + '的数据'
      set @final_sql = 'insert into GTA_ALL.dbo.L1_TRDMIN01_ALL '
      if(@tb_name like 'SH%')
        set @market_str='''SSE'''
      else
        set @market_str='''SZSE'''
      set @final_sql = @final_sql + @insert_sql + @market_str + ' as Market from ' + @db_name + '.dbo.' + @tb_name
      print '开始执行导入数据的sql语句:' + char(10) + @final_sql
      declare @isSucc int
      set @isSucc=1
      begin try
        exec(@final_sql)
      end try
      begin catch
        select ERROR_NUMBER(),ERROR_STATE(),ERROR_PROCEDURE(),ERROR_LINE(),ERROR_SEVERITY(),ERROR_MESSAGE()
        set @isSucc=-1
        print '数据库' + @db_name + '的' + @tb_name + '表导入失败'
      end catch
      if (@isSucc = 1) -- 执行过程未出现异常时将导入状态标志为1
      begin
        set @final_sql = 'update db_status set imported=1 where name='+''''+@db_name+''''
        exec(@final_sql)
        print '已成功将数据库' + @db_name + '的导入状态标记为1'
      end
      fetch next from tb_cur into @tb_name
    end
    close tb_cur
    deallocate tb_cur
    set @i=@i+1
  end
end
