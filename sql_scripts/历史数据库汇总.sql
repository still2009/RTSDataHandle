use finx_final

if object_id('dbo.import_status') is null
begin
  print '导入记录表import_status 不存在，开始创建'
  create table import_status(
    id int identity(1,1) not null,
    dbname varchar(40) not null,
    tbname varchar(40) not null,
    imported int default 0, --0代表尚未导入，1代表已经导入
    primary key(dbname,tbname)
  )
  print '表import_status 创建成功'
end
else
  print '导入记录表 import_status 已经存在'

--列出所有的历史数据库，并将其名称插入到临时表中
declare @ssql varchar(150)
declare cur cursor for select name from sys.databases
where name like 'GTA_SEL1_TRDMIN_%'

declare @temp_dbname varchar(30)
declare @temp_tbname varchar(30)
open cur
fetch next from cur into @temp_dbname
while(@@fetch_status=0)
begin
  set @ssql='declare ttb_cur cursor for select name from '+@temp_dbname+'.sys.tables where name like ''%TRDMIN01%'''
  exec(@ssql)

  open ttb_cur
  fetch next from ttb_cur into @temp_tbname
  while(@@FETCH_STATUS=0)
  begin
    if not exists(select dbname,tbname from import_status where dbname=@temp_dbname and tbname=@temp_tbname)
    begin
      print 'new table' + @temp_tbname + '插入到import_status表中'
      insert into import_status (dbname,tbname) values(@temp_dbname,@temp_tbname)
    end
	fetch next from ttb_cur into @temp_tbname
  end
  close ttb_cur
  deallocate ttb_cur

  fetch next from cur into @temp_dbname
end
close cur
deallocate cur

--列出所有未被导入总库的数据库个数
declare @not_imported_count int
select @not_imported_count=count(*) from import_status where imported=0
print '尚未导入的表的个数为 : ' + cast(@not_imported_count as varchar)


declare @db_name varchar(30), @tb_name varchar(30) ,@mysql varchar(200)
declare @market_str varchar(10)
declare @isSucc int

declare impCur cursor for select dbname,tbname from import_status where imported=0
open impCur
fetch next from impCur into @db_name,@tb_name
while(@@FETCH_STATUS=0)
begin
  set @mysql = 'insert into dbo.A_MIN_01 select SecCode,SecName,tdate,MinTime,StartPrc,HighPrc,LowPrc,EndPrc,MinTq,MinTm,'
  if(@tb_name like 'SHL1%')
    set @market_str='''SSE'''
  else if(@tb_name like 'SZL1%')
    set @market_str='''SZSE'''
  set @mysql = @mysql + @market_str + ' as Market from '+@db_name+'.dbo.'+@tb_name
  print @mysql
  set @isSucc=1
  begin try
    exec(@mysql)
  end try
  begin catch
    select ERROR_NUMBER() as errNum,ERROR_STATE() as errState,ERROR_PROCEDURE() as errProc,
	ERROR_LINE() as errLine,ERROR_SEVERITY() as errSeverity,ERROR_MESSAGE() as errMsg
    set @isSucc=-1
    print '数据库' + @db_name + '的' + @tb_name + '表导入失败'
  end catch
  if (@isSucc = 1) -- 执行过程未出现异常时将导入状态标志为1
  begin
    set @mysql = 'update import_status set imported=1 where dbname='+''''+@db_name+''' and tbname='+''''+@tb_name+''''
    print @mysql
	exec(@mysql)
    print '数据库' + @db_name + '的' + @tb_name + '表导入成功'
  end
  fetch next from impCur into @db_name,@tb_name
end
close impCur
deallocate impCur
