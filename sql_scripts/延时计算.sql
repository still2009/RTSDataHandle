use gta_update
go
/* 计算延时的sql*/
-- 零时表删除
if exists (select 1  
            from  sysobjects  
           where  id = object_id('#delay_middle')  
            and   type = 'U')  
   drop table #delay_middle
go
-- 计算每股每分钟的delay
select Symbol,ShortName,TradingDate,TradingTime,
max((ReceiveUNIX*1000-UNIX)/1000) as delay,
count(DataID) as count
into #delay_middle
from MINUTE_DATA_2016_11_02 where Freq=60
group by Symbol,ShortName,TradingDate,TradingTime
order by Symbol,ShortName

-- 合并每股每分钟的delay，计算出每股的delay
insert into Time_Delay(Symbol,ShortName,TradingDate,HighDelay,LowDelay,AvgDelay)
select Symbol,ShortName,TradingDate,
max(delay) as High_Delay,
min(delay) as Low_Delay,
avg(delay) as AVG_Delay
from #delay_middle
group by Symbol,ShortName,TradingDate
order by Symbol,ShortName

-- 零时表删除
drop table #delay_middle

-- 看每日延时的视图(已经创建)
/*create view DayDelay
as
select TradingDate,max(HighDelay) as high,avg(AvgDelay) as avg,min(LowDelay) as low
from Time_Delay
group by TradingDate*/