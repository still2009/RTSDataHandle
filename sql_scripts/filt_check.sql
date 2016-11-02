--过滤单只股票单日的行情数据的中间数据

declare @stockName
set @stockName='沪深300'

declare stockCur cursor for
select distict ShortName from [dbo].[MINUTE_DATA_2016_10_20]
-- 条数check 每天241条不同TradingTime的数据
select count(distinct TradingTime) from [dbo].[MINUTE_DATA_2016_10_20]
where ShortName=@stockName

declare cur cursor for
select max(DataID) as mid,TradingTime
from [dbo].[MINUTE_DATA_2016_10_20]
where ShortName=@stockName
group by TradingTime
order by TradingTime
