--USE [GTA_ALL]
--GO

--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '200910%' and market='SZSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '200911%' and market='SSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '201001%' and market='SSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '201002%' and market='SSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '201003%' and market='SSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '201004%' and market='SZSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '201005%' and market='SSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '201005%' and market='SZSE'
--DELETE FROM [dbo].[L1_TRDMIN01_ALL] WHERE TDATE like '201009%' and market='SZSE'   
--GO

use gta_all
drop table db_status
create table import_status(
	dbname varchar(50) not null,
	tbname varchar(50) not null,
	imported int default 0,
	primary key(dbname,tbname)
)
close db_cur
deallocate db_cur
declare db_cur cursor for select name from sys.databases where name like 'GTA_SEL1_TRDMIN%'
declare @cur_sql varchar(200)
declare @db_name varchar(50)
declare @tbname varchar(50)
open db_cur
fetch next from db_cur into @db_name
while(@@FETCH_STATUS = 0)
begin
set @cur_sql = 'declare tb_cur cursor for select name from ' + @db_name + '.sys.tables where name like ''%TRDMIN01%'''
print @cur_sql
exec(@cur_sql)
open tb_cur
fetch next from tb_cur into @tbname
while(@@FETCH_STATUS = 0)
begin
insert into import_status values(@db_name,@tbname,1)
fetch next from tb_cur into @tbname
end
close tb_cur
deallocate tb_cur
fetch next from db_cur into @db_name
end
