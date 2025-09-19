const base_url = "https://www.basketball-reference.com/";
const axios = require("axios");
const cheerio = require("cheerio");
const mysql = require("mysql2/promise");
const fs = require("fs"); // Require the file system module to read the SSL certificate file

// #region COMMON FUNCTIONS
function formatISOString(strDate) {
  let d = new Date(strDate);
  return d.toISOString().split("T")[0];
}

function toMilitaryTime(time12) {
  // Split the input string into hours, minutes, and AM/PM parts
  var [time, period] = time12.split(/([ap])/i);

  // Parse the hours and minutes
  var [hours, minutes] = time.split(":").map(Number);

  // If the period is 'p' (PM) and the hours are less than 12, add 12 to the hours
  if (period.toLowerCase() === "p" && hours < 12) {
    hours += 12;
  }

  // If the period is 'a' (AM) and the hours are 12, set the hours to 0 (midnight)
  if (period.toLowerCase() === "a" && hours === 12) {
    hours = 0;
  }

  // Ensure the hours are in 24-hour format (0-23)
  hours = hours % 24;

  // Format the hours and minutes as 'HH:mm'
  var time24 = `${String(hours).padStart(2, "0")}:${String(minutes).padStart(
    2,
    "0"
  )}`;

  return time24;
}
function insert_json(data, filename) {
  // Get  json data
  const fs = require("fs");
  if (!fs.existsSync(filename)) {
    fs.writeFileSync(filename, JSON.stringify(data));
  } else {
    fs.appendFileSync(filename, "\n" + JSON.stringify(data));
  }
}
// #endregion

/**
 * Use this function
 * @param {number} start_year start year of the one season we are processing
 */
async function get_games(start_year) {
  const season_url = `${base_url.slice(0, -1)}/leagues/NBA_${(
    start_year + 1
  ).toString()}_games.html`;

  // default page is only the first month's games
  var month_games = await axios.get(season_url);
  $ = cheerio.load(month_games.data);

  // Get the urls to access the games of the rest of the months
  var all_months_urls = [season_url];
  $(".filter div:not(.current)").each(function (y, z) {
    var href = $(z).find("a").attr("href");
    if (href) {
      all_months_urls.push(href);
    }
  });

  // FOR EACH MONTH
  let first_page = true;
  for (const month_url of all_months_urls) {
    if (first_page) {
      first_page = false;
    } else {
      await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE
      month_games = await axios.get(base_url.slice(0, -1) + month_url);
      $ = cheerio.load(month_games.data);
    }

    const all_games_season = $("table#schedule tbody tr:not(.thead)");
    var no_more_games = false;
    for (const game_row of all_games_season) {
      if (no_more_games) break; //! BREAK
      /**************************
       * Collect basic game data
       */
      // #region
      console.log("***-------------------------");
      var game = {};
      const columns = $(game_row).find("td");
      try {
        let date = $(game_row).find("th").text();
        date = formatISOString(date);
        let time = $(columns[0]).text();
        time = toMilitaryTime(time);
        game["date_time"] = date + "T" + time;
        console.log("Date + Time: " + game["date_time"]);
      } catch (error) {
        game["date_time"] = null;
        console.log("date_time Error: " + error);
      }
      try {
        game["away_team_br_id"] = $(columns[1])
          .find("a")
          .prop("href")
          .match(/\/(\w+)\/\d+\.html/)[1];
        console.log("away_team_br_id: " + game["away_team_br_id"]);
      } catch (error) {
        game["away_team_br_id"] = null;
        console.log("away_team_br_id Error: " + error);
      }
      try {
        game["away_team_points"] = $(columns[2]).text();
        console.log("away_team_points: " + game["away_team_points"]);
      } catch (error) {
        game["away_team_points"] = null;
        console.log("away_team_points Error: " + error);
      }
      try {
        game["home_team_br_id"] = $(columns[3])
          .find("a")
          .prop("href")
          .match(/\/(\w+)\/\d+\.html/)[1];
        console.log("home_team_br_id: " + game["home_team_br_id"]);
      } catch (error) {
        game["home_team_br_id"] = null;
        console.log("home_team_br_id Error: " + error);
      }
      try {
        game["home_team_points"] = $(columns[4]).text();
        console.log("home_team_points: " + game["home_team_points"]);
      } catch (error) {
        game["home_team_points"] = null;
        console.log("home_team_points Error: " + error);
      }
      // TODO improve by checking instead if the game has completed rather than checking if there are no points
      if (game["away_team_points"] === "" && game["home_team_points"] === "") {
        console.log(`No more games in season as of ${game["date_time"]}`);
        no_more_games = true;
        break; //! BREAK
      }
      try {
        game["ot"] = $(columns[6]).text();
        console.log("ot: " + game["ot"]);
      } catch (error) {
        game["ot"] = null;
        console.log("ot Error: " + error);
      }
      try {
        game["attendance"] = $(columns[7]).text().replace(",", "");
        console.log("attendance: " + game["attendance"]);
      } catch (error) {
        game["attendance"] = null;
        console.log("attendance Error: " + error);
      }
      try {
        game["game_duration"] = $(columns[8]).text();
        console.log("game_duration: " + game["game_duration"]);
      } catch (error) {
        game["game_duration"] = null;
        console.log("game_duration Error: " + error);
      }
      try {
        game["arena"] = $(columns[9]).text();
        console.log("arena: " + game["arena"]);
      } catch (error) {
        game["arena"] = null;
        console.log("arena Error: " + error);
      }
      // #endregion

      /**********************************
       * Collect detailed game data
       */
      // #region
      console.log("-------------------------");
      try {
        let game_details_page =
          base_url.slice(0, -1) + $(columns[5]).find("a").prop("href");
        game["url"] = game_details_page;
        console.log("url: " + game["url"]);
        await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE

        var game_details_response = await axios.get(game_details_page);
        $ = cheerio.load(game_details_response.data);

        try {
          game["br_id"] = game_details_page.split("/")[4].replace(".html", "");
          console.log("br_id: " + game["br_id"]);
        } catch (error) {
          game["br_id"] = null;
          console.log("br_id Error: " + error);
        }

        // inactive players
        try {
          let inactive_players = [];
          inactive_starting_element = $("#content strong").filter(function () {
            return $(this).text().includes("Inactive:");
          });
          if (inactive_starting_element.length != 0) {
            inactive_starting_element = inactive_starting_element.parent();
            for (const inactive_a_tag of inactive_starting_element.find("a")) {
              inactive_players.push(
                $(inactive_a_tag)
                  .prop("href")
                  .split("/")[3]
                  .replace("html", "")
                  .replace(".", "")
              );
            }
          }
          game["inactive_players"] = inactive_players;
          console.log("inactive_players: " + game["inactive_players"]);
        } catch (error) {
          game["inactive_players"] = null;
          console.log("inactive_players Error: " + error);
        }

        // officials
        try {
          let officials = [];
          officials_starting_element = $("#content strong").filter(function () {
            return $(this).text().includes("Officials:");
          });
          if (officials_starting_element.length != 0) {
            officials_starting_element = officials_starting_element.parent();
            for (const officials_a_tag of officials_starting_element.find(
              "a"
            )) {
              officials.push(
                $(officials_a_tag)
                  .prop("href")
                  .split("/")[2]
                  .replace(".html", "")
              );
            }
          }
          game["officials"] = officials;
          console.log("officials: " + game["officials"]);
        } catch (error) {
          game["officials"] = null;
          console.log("officials Error: " + error);
        }

        // game duration
        try {
          let game_duration_temp = $("#content strong")
            .filter(function () {
              return $(this).text().includes("Time of Game:");
            })
            .parent()
            .text();
          game["game_duration"] =
            game_duration_temp.match(/(\d{1,2}:\d{2})/)?.[0];
          console.log("game_duration: " + game["game_duration"]);
        } catch (error) {
          game["game_duration"] = null;
          console.log("game_duration Error: " + error);
        }
      } catch (error) {
        console.log("CRITICAL ERROR (no game details retrieved): " + error);
      }
      // #endregion
      console.log("-------------------------***\n\n");
      if (JSON.stringify(game) != "" && game.home_team_points != "") {
        // TODO improve this to more accurately exclude incomplete games
        insert_json(game, "games.jsonl");
      }
    }
  }
}

/**
 * One or all of the get_games functions are not handling the scenario when there are no inactive players
 */
async function get_games_all_seasons2() {
  /******************************************** */
  /******************************************** */
  /** CONTROLS **/
  const SEASONS_SKIP = 33; // 0

  /*
        *
            <= 1999
        game_duration
            <= 2006-10-31T20:00
    */
  console.log("BEGIN async function get_games2()");

  // URL of the webpage containing the table
  const url = base_url + "leagues/";

  try {
    /**
     * Collect seasons data
     */
    const response1 = await axios.get(url);

    if (response1.status === 200) {
      var $ = cheerio.load(response1.data);
      const table = $("table.stats_table");
      const seasons_rows = table.find("tbody tr:not(.haha)");
      for (const season_row of seasons_rows) {
        const season_row_element = $(season_row);

        if (season_row_element.index() < 2 + SEASONS_SKIP) continue; // Skip the two header rows
        const next_page =
          base_url.slice(0, -1) +
          season_row_element.find("th > a").prop("href").replace(".html", "") +
          "_games.html";

        await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE

        // default page is only the first month's games
        var month_games = await axios.get(next_page);
        $ = cheerio.load(month_games.data);

        // Get the urls to access the games of the rest of the months
        var all_months_urls = [next_page];
        $(".filter div:not(.current)").each(function (y, z) {
          var href = $(z).find("a").attr("href");
          if (href) {
            all_months_urls.push(href);
          }
        });

        let first_page = true;
        for (const month_url of all_months_urls) {
          if (first_page) {
            first_page = false;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE
            month_games = await axios.get(base_url.slice(0, -1) + month_url);
            $ = cheerio.load(month_games.data);
          }

          const all_games_season = $("table#schedule tbody tr:not(.thead)");
          var no_more_games = false;
          for (const game_row of all_games_season) {
            if (no_more_games) break; //! BREAK
            /**************************
             * Collect basic game data
             */
            // #region
            console.log("***-------------------------");
            var game = {};
            const columns = $(game_row).find("td");
            try {
              let date = $(game_row).find("th").text();
              date = formatISOString(date);
              game["date_time"] = date + "T00:00:00";
              console.log("Date + Time: " + game["date_time"]);
            } catch (error) {
              game["date_time"] = null;
              console.log("date_time Error: " + error);
            }
            try {
              game["away_team_br_id"] = $(columns[0])
                .find("a")
                .prop("href")
                .match(/\/(\w+)\/\d+\.html/)[1];
              console.log("away_team_br_id: " + game["away_team_br_id"]);
            } catch (error) {
              game["away_team_br_id"] = null; //!
              console.log("away_team_br_id Error: " + error);
            }
            try {
              game["away_team_points"] = $(columns[1]).text();
              console.log("away_team_points: " + game["away_team_points"]);
            } catch (error) {
              game["away_team_points"] = null;
              console.log("away_team_points Error: " + error);
            }
            try {
              game["home_team_br_id"] = $(columns[2])
                .find("a")
                .prop("href")
                .match(/\/(\w+)\/\d+\.html/)[1];
              console.log("home_team_br_id: " + game["home_team_br_id"]);
            } catch (error) {
              game["home_team_br_id"] = null; //!
              console.log("home_team_br_id Error: " + error);
            }
            try {
              game["home_team_points"] = $(columns[3]).text();
              console.log("home_team_points: " + game["home_team_points"]);
            } catch (error) {
              game["home_team_points"] = null;
              console.log("home_team_points Error: " + error);
            }
            // // TODO improve by checking instead if the game has completed rather than checking if there are no points
            // if (game['away_team_points'] === '' && game['home_team_points'] === '') {
            //     console.log(`No more games in season as of ${game['date_time']}`);
            //     no_more_games = true;
            //     break; //! BREAK
            // }
            try {
              game["ot"] = $(columns[5]).text();
              console.log("ot: " + game["ot"]);
            } catch (error) {
              game["ot"] = null;
              console.log("ot Error: " + error);
            }
            try {
              game["attendance"] = $(columns[6]).text().replace(",", "");
              console.log("attendance: " + game["attendance"]);
            } catch (error) {
              game["attendance"] = null;
              console.log("attendance Error: " + error);
            }
            try {
              game["arena"] = $(columns[7]).text();
              console.log("arena: " + game["arena"]);
            } catch (error) {
              game["arena"] = null;
              console.log("arena Error: " + error);
            }
            // #endregion

            /**********************************
             * Collect detailed game data
             */
            // #region
            console.log("-------------------------");
            try {
              let game_details_page =
                base_url.slice(0, -1) + $(columns[4]).find("a").prop("href");
              game["url"] = game_details_page;
              console.log("url: " + game["url"]);
              await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE

              var game_details_response = await axios.get(game_details_page);
              $ = cheerio.load(game_details_response.data);

              try {
                game["br_id"] = game_details_page
                  .split("/")[4]
                  .replace(".html", "");
                console.log("br_id: " + game["br_id"]);
              } catch (error) {
                game["br_id"] = null;
                console.log("br_id Error: " + error);
              }

              // inactive players
              try {
                let inactive_players = [];
                inactive_starting_element = $("#content strong").filter(
                  function () {
                    return $(this).text().includes("Inactive:");
                  }
                );
                if (inactive_starting_element.length != 0) {
                  inactive_starting_element =
                    inactive_starting_element.parent();
                  for (const inactive_a_tag of inactive_starting_element.find(
                    "a"
                  )) {
                    inactive_players.push(
                      $(inactive_a_tag)
                        .prop("href")
                        .split("/")[3]
                        .replace("html", "")
                        .replace(".", "")
                    );
                  }
                }
                game["inactive_players"] = inactive_players;
                console.log("inactive_players: " + game["inactive_players"]);
              } catch (error) {
                game["inactive_players"] = null;
                console.log("inactive_players Error: " + error);
              }

              // officials
              try {
                let officials = [];
                officials_starting_element = $("#content strong").filter(
                  function () {
                    return $(this).text().includes("Officials:");
                  }
                );
                if (officials_starting_element.length != 0) {
                  officials_starting_element =
                    officials_starting_element.parent();
                  for (const officials_a_tag of officials_starting_element.find(
                    "a"
                  )) {
                    officials.push(
                      $(officials_a_tag)
                        .prop("href")
                        .split("/")[2]
                        .replace(".html", "")
                    );
                  }
                }
                game["officials"] = officials;
                console.log("officials: " + game["officials"]);
              } catch (error) {
                game["officials"] = null;
                console.log("officials Error: " + error);
              }

              // game duration
              try {
                let game_duration_temp = $("#content strong")
                  .filter(function () {
                    return $(this).text().includes("Time of Game:");
                  })
                  .parent()
                  .text();
                game["game_duration"] =
                  game_duration_temp.match(/(\d{1,2}:\d{2})/)?.[0];
                console.log("game_duration: " + game["game_duration"]);
              } catch (error) {
                game["game_duration"] = null;
                console.log("game_duration Error: " + error);
              }
            } catch (error) {
              console.log(
                "CRITICAL ERROR (no game details retrieved): " + error
              );
            }
            // #endregion
            console.log("-------------------------***\n\n");
            if (JSON.stringify(game) != "" && game.home_team_points != "") {
              // TODO improve this to more accurately exclude incomplete games
              insert_json(game, "games2.jsonl");
            }
          }
        }
      }
    } else {
      console.log("Failed to download the HTML content");
    }
  } catch (error) {
    console.log("Error: " + error);
  }
  console.log("END async function get_games1()");
}

/**
 * One or all of the get_games functions are not handling the scenario when there are no inactive players
 */
async function get_games_all_seasons3() {
  /******************************************** */
  /******************************************** */
  /** CONTROLS **/
  const SEASONS_SKIP = 38; // 0
  console.log("BEGIN async function get_games1()");

  // URL of the webpage containing the table
  const url = base_url + "leagues/";

  try {
    /**
     * Collect seasons data
     */
    const response1 = await axios.get(url);

    if (response1.status === 200) {
      var $ = cheerio.load(response1.data);
      const table = $("table.stats_table");
      const seasons_rows = table.find("tbody tr:not(.haha)");
      for (const season_row of seasons_rows) {
        const season_row_element = $(season_row);

        if (season_row_element.index() < 2 + SEASONS_SKIP) continue; // Skip the two header rows
        const next_page =
          base_url.slice(0, -1) +
          season_row_element.find("th > a").prop("href").replace(".html", "") +
          "_games.html";

        await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE

        // default page is only the first month's games
        var month_games = await axios.get(next_page);
        $ = cheerio.load(month_games.data);

        // Get the urls to access the games of the rest of the months
        var all_months_urls = [next_page];
        $(".filter div:not(.current)").each(function (y, z) {
          var href = $(z).find("a").attr("href");
          if (href) {
            all_months_urls.push(href);
          }
        });

        let first_page = true;
        for (const month_url of all_months_urls) {
          if (first_page) {
            first_page = false;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE
            month_games = await axios.get(base_url.slice(0, -1) + month_url);
            $ = cheerio.load(month_games.data);
          }

          const all_games_season = $("table#schedule tbody tr:not(.thead)");
          var no_more_games = false;
          for (const game_row of all_games_season) {
            if (no_more_games) break; //! BREAK
            /**************************
             * Collect basic game data
             */
            // #region
            console.log("***-------------------------");
            var game = {};
            const columns = $(game_row).find("td");
            try {
              let date = $(game_row).find("th").text();
              date = formatISOString(date);
              game["date_time"] = date + "T00:00:00";
              console.log("Date + Time: " + game["date_time"]);
            } catch (error) {
              game["date_time"] = null;
              console.log("date_time Error: " + error);
            }
            try {
              game["away_team_br_id"] = $(columns[1])
                .find("a")
                .prop("href")
                .match(/\/(\w+)\/\d+\.html/)[1];
              console.log("away_team_br_id: " + game["away_team_br_id"]);
            } catch (error) {
              game["away_team_br_id"] = null; //!
              console.log("away_team_br_id Error: " + error);
            }
            try {
              game["away_team_points"] = $(columns[2]).text();
              console.log("away_team_points: " + game["away_team_points"]);
            } catch (error) {
              game["away_team_points"] = null;
              console.log("away_team_points Error: " + error);
            }
            try {
              game["home_team_br_id"] = $(columns[3])
                .find("a")
                .prop("href")
                .match(/\/(\w+)\/\d+\.html/)[1];
              console.log("home_team_br_id: " + game["home_team_br_id"]);
            } catch (error) {
              game["home_team_br_id"] = null; //!
              console.log("home_team_br_id Error: " + error);
            }
            try {
              game["home_team_points"] = $(columns[4]).text();
              console.log("home_team_points: " + game["home_team_points"]);
            } catch (error) {
              game["home_team_points"] = null;
              console.log("home_team_points Error: " + error);
            }
            // // TODO improve by checking instead if the game has completed rather than checking if there are no points
            // if (game['away_team_points'] === '' && game['home_team_points'] === '') {
            //     console.log(`No more games in season as of ${game['date_time']}`);
            //     no_more_games = true;
            //     break; //! BREAK
            // }
            try {
              game["ot"] = $(columns[6]).text();
              console.log("ot: " + game["ot"]);
            } catch (error) {
              game["ot"] = null;
              console.log("ot Error: " + error);
            }
            try {
              game["attendance"] = $(columns[7]).text().replace(",", "");
              console.log("attendance: " + game["attendance"]);
            } catch (error) {
              game["attendance"] = null;
              console.log("attendance Error: " + error);
            }
            try {
              game["arena"] = $(columns[8]).text();
              console.log("arena: " + game["arena"]);
            } catch (error) {
              game["arena"] = null;
              console.log("arena Error: " + error);
            }
            // #endregion

            /**********************************
             * Collect detailed game data
             */
            // #region
            console.log("-------------------------");
            try {
              let game_details_page =
                base_url.slice(0, -1) + $(columns[5]).find("a").prop("href");
              game["url"] = game_details_page;
              console.log("url: " + game["url"]);
              await new Promise((resolve) => setTimeout(resolve, 4000)); //! PAUSE

              var game_details_response = await axios.get(game_details_page);
              $ = cheerio.load(game_details_response.data);

              try {
                game["br_id"] = game_details_page
                  .split("/")[4]
                  .replace(".html", "");
                console.log("br_id: " + game["br_id"]);
              } catch (error) {
                game["br_id"] = null;
                console.log("br_id Error: " + error);
              }

              // inactive players
              try {
                let inactive_players = [];
                inactive_starting_element = $("#content strong").filter(
                  function () {
                    return $(this).text().includes("Inactive:");
                  }
                );
                if (inactive_starting_element.length != 0) {
                  inactive_starting_element =
                    inactive_starting_element.parent();
                  for (const inactive_a_tag of inactive_starting_element.find(
                    "a"
                  )) {
                    inactive_players.push(
                      $(inactive_a_tag)
                        .prop("href")
                        .split("/")[3]
                        .replace("html", "")
                        .replace(".", "")
                    );
                  }
                }
                game["inactive_players"] = inactive_players;
                console.log("inactive_players: " + game["inactive_players"]);
              } catch (error) {
                game["inactive_players"] = null;
                console.log("inactive_players Error: " + error);
              }

              // officials
              try {
                let officials = [];
                officials_starting_element = $("#content strong").filter(
                  function () {
                    return $(this).text().includes("Officials:");
                  }
                );
                if (officials_starting_element.length != 0) {
                  officials_starting_element =
                    officials_starting_element.parent();
                  for (const officials_a_tag of officials_starting_element.find(
                    "a"
                  )) {
                    officials.push(
                      $(officials_a_tag)
                        .prop("href")
                        .split("/")[2]
                        .replace(".html", "")
                    );
                  }
                }
                game["officials"] = officials;
                console.log("officials: " + game["officials"]);
              } catch (error) {
                game["officials"] = null;
                console.log("officials Error: " + error);
              }

              // game duration
              try {
                let game_duration_temp = $("#content strong")
                  .filter(function () {
                    return $(this).text().includes("Time of Game:");
                  })
                  .parent()
                  .text();
                game["game_duration"] =
                  game_duration_temp.match(/(\d{1,2}:\d{2})/)?.[0];
                console.log("game_duration: " + game["game_duration"]);
              } catch (error) {
                game["game_duration"] = null;
                console.log("game_duration Error: " + error);
              }
            } catch (error) {
              console.log(
                "CRITICAL ERROR (no game details retrieved): " + error
              );
            }
            // #endregion
            console.log("-------------------------***\n\n");
            if (JSON.stringify(game) != "" && game.home_team_points != "") {
              // TODO improve this to more accurately exclude incomplete games
              insert_json(game, "games3.jsonl");
            }
          }
        }
      }
    } else {
      console.log("Failed to download the HTML content");
    }
  } catch (error) {
    console.log("Error: " + error);
  }
  console.log("END async function get_games1()");
}

get_games(2024);
