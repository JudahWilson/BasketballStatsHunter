"use strict";
/**
 *
 * @param type FilterCategories
 * @returns Filter
 */
function filter_factory(type) {
    if (type == "player") {
        return new PlayerFilter(type);
    }
    else if (type == "game") {
        return new GameFilter(type);
    }
    else if (type == "team") {
        return new TeamFilter(type);
    }
    else if (type == "season") {
        return new SeasonFilter(type);
    }
    else if (type == "all-time") {
        return new AllTimeFilter(type);
    }
    else if (type == "date") {
        return new DateFilter(type);
    }
    else {
        throw new Error("Invalid filter type");
    }
}
class PlayerFilter {
    constructor(type) {
        this.type = type;
    }
    apply() {
        console.log("PlayerFilter!");
        return [];
    }
}
class GameFilter {
    constructor(type) {
        this.type = type;
    }
    apply() {
        console.log("GameFilter!");
        return [];
    }
}
class TeamFilter {
    constructor(type) {
        this.type = type;
    }
    apply() {
        console.log("TeamFilter!");
        return [];
    }
}
class SeasonFilter {
    constructor(type) {
        this.type = type;
    }
    apply() {
        console.log("SeasonFilter!");
        return [];
    }
}
class AllTimeFilter {
    constructor(type) {
        this.type = type;
    }
    apply() {
        console.log("AllTimeFilter!");
        return [];
    }
}
class DateFilter {
    constructor(type) {
        this.type = type;
    }
    apply() {
        console.log("DateFilter!");
        return [];
    }
}
/* #endregion */ 
