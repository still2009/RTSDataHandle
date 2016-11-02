use [GTA_UPDATE]
create table [dbo].[SZL1_TRDMIN01](
    [SecurityID] bigint,
    [TradeTime] datetime,
    [ProductID] bigint,
    [Symbol] varchar(6) COLLATE Chinese_PRC_CI_AS NOT NULL,
    [ShortName] varchar(20) COLLATE Chinese_PRC_CI_AS NOT NULL,
    [TradingDate] date,
    [TradingTime] datetime,
    [UNIX] bigint,
    [Market] nvarchar(4) COLLATE Chinese_PRC_CI_AS NOT NULL,
    [OpenPrice] decimal(9,3),
    [HighPrice] decimal(9,3),
    [LowPrice] decimal(9,3),
    [ClosePrice] decimal(9,3),
    [Volume] decimal(12,0),
    [Amount] decimal(18,3),
    [BenchMarkOpenPrice] decimal(9,3),
    [Change] decimal(9,3),
    [ChangeRatio] decimal(9,4),
    [TotalVolume] bigint,
    [VWAP] decimal(9,3),
    [CumulativeLowPrice] decimal(9,3),
    [CumulativeHighPrice] decimal(9,3),
    [CumulativeVWAP] decimal(9,3)
)
ON [PRIMARY]
GO
