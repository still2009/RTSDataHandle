DECLARE @i int
DECLARE @c char(6)
declare @prefix varchar(20)
declare @sql varchar(200)
declare @uname varchar(20)
declare @pwd varchar(20)
declare @dbrole varchar(20)
set @uname='finx03'
set @pwd='finx-c0mm0n'
--创建登陆帐户（create login）
set @sql='create login ' + @uname + ' with password='''+ @pwd +''', default_database=master'
print @sql
exec(@sql)
--为登陆账户创建数据库用户
set @sql='create user '+ @uname +' for login '+ @uname +' with default_schema=dbo'
print @sql

--授权
set @dbrole='db_datareader'
set @prefix='GTA_SEL1_TRDMIN_'
-- gta_qdb
set @sql='use [GTA_QDB];CREATE USER [' + @uname + '] FOR LOGIN [' + @uname + '];ALTER ROLE [' + @dbrole + '] ADD MEMBER [' + @uname + ']'
exec(@sql)
--历史数据库
set @i= 1
while @i <= 164
begin
set @c=(select CONVERT(char(6),DATEADD(month, @i, '2002-12-1'), 112))
set @sql='use [' + @prefix + @c + '];CREATE USER [' + @uname + '] FOR LOGIN [' + @uname + '];ALTER ROLE [' + @dbrole + '] ADD MEMBER [' + @uname + ']'
exec(@sql)
set @i=@i+1
end
