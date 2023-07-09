type FilterCategories = "player" | "game" | "team" | "season" | "all-time" | "date"



/* =========================================== */
// Filters
/* =========================================== */
/* #region  */
interface Filter {
  apply(): []
}
/**
 * 
 * @param type FilterCategories
 * @returns Filter
 */
function filter_factory(type: FilterCategories): Filter {
  if (type == "player") {
    return new PlayerFilter(type)
  } else if (type == "game") {
    return new GameFilter(type)
  } else if (type == "team") {
    return new TeamFilter(type)
  } else if (type == "season") {
    return new SeasonFilter(type)
  } else if (type == "all-time") {
    return new AllTimeFilter(type)
  } else if (type == "date") {
    return new DateFilter(type)
  } else {
    throw new Error("Invalid filter type")
  }
}

class PlayerFilter implements Filter {
  type: string;

  constructor(type: string) {
    this.type = type;
  }

  apply(): [] {
    console.log("PlayerFilter!");
    return [];
  }
}

class GameFilter implements Filter {
  type: string;

  constructor(type: string) {
    this.type = type;
  }

  apply(): [] {
    console.log("GameFilter!");
    return [];
  }
}

class TeamFilter implements Filter {
  type: string;

  constructor(type: string) {
    this.type = type;
  }

  apply(): [] {
    console.log("TeamFilter!");
    return [];
  }
}

class SeasonFilter implements Filter {
  type: string;

  constructor(type: string) {
    this.type = type;
  }

  apply(): [] {
    console.log("SeasonFilter!");
    return [];
  }
}

class AllTimeFilter implements Filter {
  type: string;

  constructor(type: string) {
    this.type = type;
  }

  apply(): [] {
    console.log("AllTimeFilter!");
    return [];
  }
}

class DateFilter implements Filter {
  type: string;

  constructor(type: string) {
    this.type = type;
  }

  apply(): [] {
    console.log("DateFilter!");
    return [];
  }
}
/* #endregion */