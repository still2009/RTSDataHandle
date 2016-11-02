declare @basespath varchar(100)
declare @BeginMonth varchar(6)
declare @EndMonth varchar(6)
declare @DataPartName varchar(100)

--�������ݿ��ļ������ļ���
set @basespath='D:\����L1��ʱ'
--���ÿ�ʼ�·�
set @BeginMonth = '200301'
--���ý����·�
set @EndMonth = '201608'
--��������Ʒ��
set @DataPartName = 'GTA%'

declare @MaxId int,@CurId int
declare @DBName varchar(200)
declare @Sql_tt varchar(2000)


--��ȡĿ��·���µ��ļ�����mdf����GTA��׺�ģ�ƴ�Ӹ������ݿ����
if exists (select * from master..sysobjects where xtype='U' and name ='##tempDBname_tt')
	drop table ##tempDBname_tt
if exists (select * from master..sysobjects where xtype='U' and name ='tempDBFile_tt')
	drop table ##tempDBFile_tt	
	
create table ##tempDBname_tt
(
	name nvarchar(200),
	depth int,
	[file] int
)
create table ##tempDBFile_tt
(
	id int identity,
	DBName varchar(200),
	DBFileName varchar(200),
	ordertext varchar(2000)
)

set @Sql_tt='insert into ##tempDBname_tt exec master..xp_dirtree '''+@basespath+''',1,1'
exec(@Sql_tt)



insert into ##tempDBFile_tt select substring(name,1,len(name)-4) DBName,name DBFileName,name ordertext from ##tempDBname_tt
where name like '%.GTA' or name like '%.mdf'

delete from ##tempDBFile_tt 
where DBName not like @DataPartName or right(DBName,6)<@BeginMonth or right(DBName,6)>@EndMonth

update ##tempDBFile_tt set ordertext = ('sp_attach_db '''+upper(DBName)+''', '''+@basespath+'\'+DBFileName+''', '''+@basespath+'\'+DBName+'_log.ldf''')

--��ѯִ�и������ݿ�
set @Sql_tt = convert(varchar(25),getdate(),121)+' ** ���ݿ⸽�ӿ�ʼ...'
print(@Sql_tt)
select  @CurId=min(id),@MaxId=max(id) from ##tempDBFile_tt

while (@CurId <= @MaxId)
begin
	select @DBName=DBName, @Sql_tt=ordertext from ##tempDBFile_tt where id = @CurId
	if not exists(select 1 from master.dbo.sysdatabases where name=@DBName)
	begin
		exec(@Sql_tt)
		set @Sql_tt = convert(varchar(25),getdate(),121)+' ** ���ݿ�'+@DBName+'���ӽ���...'
		print(@Sql_tt)
	end
	else
	begin
		set @Sql_tt = convert(varchar(25),getdate(),121)+' ** ���ݿ�'+@DBName+'�ڱ�ʵ�����Ѿ����ڣ����ܸ���'
		print(@Sql_tt)
	end
	set @CurId=@CurId+1
end

--ִ�����
set @Sql_tt = convert(varchar(25),getdate(),121)+' ** ���ݿ⸽�ӽ���...'
print(@Sql_tt)
drop table ##tempDBname_tt
drop table ##tempDBFile_tt
