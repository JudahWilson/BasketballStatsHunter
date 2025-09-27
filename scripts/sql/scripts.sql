-- Total per game stats row count
select (
        select count(*)
        from playergamestats
    ) + (
        select count(*)
        from playergamequarterstats
    ) + (
        select count(*)
        from playergamehalfstats
    ) + (
        select count(*)
        from playergameovertimestats
    ) + (
        select count(*)
        from teamgamestats
    ) + (
        select count(*)
        from teamgamequarterstats
    ) + (
        select count(*)
        from teamgamehalfstats
    ) + (
        select count(*)
        from teamgamequarterstats
    ) + (
        select count(*)
        from teamgameovertimestats
    ) as "Per-game stats row count";