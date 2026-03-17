# Market Hours & Extended Trading (Updated 2026-03-08)

## Standard Trading Hours (US Equities)
- **Time Zone**: Eastern Time (ET)
- **Market Open**: 09:30 AM ET
- **Market Close**: 04:00 PM ET

## Extended Hours (Alpaca Support)
Alpaca supports extended hours for all symbols, with the following schedule (all times Eastern):
- **Pre-Market**: 04:00 AM – 09:30 AM ET (Mon-Fri)
- **After-Hours**: 04:00 PM – 08:00 PM ET (Mon-Fri)
- **Overnight (24/5)**: 08:00 PM – 04:00 AM ET (Sun-Fri)

### Technical Requirements for Extended Hours
- **Order Type**: Must be a **Limit Order**.
- **Time in Force**: Must be **Day** or **GTC**.
- **Param**: Must set `extended_hours=True` in the API call.

## Weekend Status
- **Saturday**: Fully closed (No pre/post/overnight).
- **Sunday**: Core closed; Overnight opens at 08:00 PM ET.

## Strategic Notes
- **Webull Comparison**: Webull offers 24-hour trading on select stocks; Alpaca’s **24/5** covers the overnight gap (8pm-4am) for all symbols supported by their overnight venue.
- **Liquidity Warning**: Spreads are wider and liquidity is lower during extended/overnight hours.
- **WULF Context**: WULF is eligible for these extended sessions on Alpaca.
