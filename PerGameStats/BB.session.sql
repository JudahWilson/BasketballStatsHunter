select "playergamestats" as "table", count(*) from playergamestats
union select "playergamestats" as "table", count(*) from playergamestats
union select "playergamequarterstats" as "table", count(*) from playergamequarterstats
union select "playergamequarterstats" as "table", count(*) from playergamequarterstats
union select "playergamehalfstats" as "table", count(*) from playergamehalfstats
union select "playergamehalfstats" as "table", count(*) from playergamehalfstats
union select "teamgamestats" as "table", count(*) from teamgamestats
union select "teamgamestats" as "table", count(*) from teamgamestats
union select "teamgamequarterstats" as "table", count(*) from teamgamequarterstats
union select "teamgamequarterstats" as "table", count(*) from teamgamequarterstats
union select "teamgamehalfstats" as "table", count(*) from teamgamehalfstats
union select "teamgamehalfstats" as "table", count(*) from teamgamehalfstats
union select "teamgamequarterstats" as "table", count(*) from teamgamequarterstats
union select "teamgamequarterstats" as "table", count(*) from teamgamequarterstats;

select "FIRST playergamestats" as "table", min(game_br_id) as "game_br_id" from playergamestats
union select "LAST playergamestats" as "table", max(game_br_id) as "game_br_id" from playergamestats
union select "FIRST teamgamestats" as "table", min(game_br_id) as "game_br_id" from teamgamestats
union select "LAST teamgamestats" as "table", max(game_br_id) as "game_br_id" from teamgamestats;

select "FIRST playergamestats" as "table", min(game_br_id) as "game_br_id" from playergamestats
union select "LAST playergamestats" as "table", max(game_br_id) as "game_br_id" from playergamestats
union select "FIRST playergamequarterstats" as "table", min(game_br_id) as "game_br_id" from playergamequarterstats
union select "LAST playergamequarterstats" as "table", max(game_br_id) as "game_br_id" from playergamequarterstats
union select "FIRST playergamehalfstats" as "table", min(game_br_id) as "game_br_id" from playergamehalfstats
union select "LAST playergamehalfstats" as "table", max(game_br_id) as "game_br_id" from playergamehalfstats
union select "FIRST teamgamestats" as "table", min(game_br_id) as "game_br_id" from teamgamestats
union select "LAST teamgamestats" as "table", max(game_br_id) as "game_br_id" from teamgamestats
union select "FIRST teamgamequarterstats" as "table", min(game_br_id) as "game_br_id" from teamgamequarterstats
union select "LAST teamgamequarterstats" as "table", max(game_br_id) as "game_br_id" from teamgamequarterstats
union select "FIRST teamgamehalfstats" as "table", min(game_br_id) as "game_br_id" from teamgamehalfstats
union select "LAST teamgamehalfstats" as "table", max(game_br_id) as "game_br_id" from teamgamehalfstats
union select "FIRST teamgamequarterstats" as "table", min(game_br_id) as "game_br_id" from teamgamequarterstats
union select "LAST teamgamequarterstats" as "table", max(game_br_id) as "game_br_id" from teamgamequarterstats;


select 
(select count(*) from playergamestats)
+ (select count(*) from playergamestats)
+ (select count(*) from playergamequarterstats)
+ (select count(*) from playergamequarterstats)
+ (select count(*) from playergamehalfstats)
+ (select count(*) from playergamehalfstats)
+ (select count(*) from teamgamestats)
+ (select count(*) from teamgamestats)
+ (select count(*) from teamgamequarterstats)
+ (select count(*) from teamgamequarterstats)
+ (select count(*) from teamgamehalfstats)
+ (select count(*) from teamgamehalfstats)
+ (select count(*) from teamgamequarterstats)
+ (select count(*) from teamgamequarterstats) as total_count;