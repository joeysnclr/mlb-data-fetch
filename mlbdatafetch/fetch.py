from datatypes import EntryList, Game, Player, Team, Venue, DefensePlay, Pitch, BatterBoxscore, PitcherBoxscore, GamefeedResponse
from utils import get_request_json

def players(sport_id: int = 1, season: int = 2024) -> EntryList[Player]:
    players_url = f"https://statsapi.mlb.com/api/v1/sports/{sport_id}/players"
    params = {
        'season': str(season),
    }
    players_raw = get_request_json(players_url, params).get('people')
    players_clean = EntryList(Player(
        id=p.get('id'),
        full_name=p.get('fullName'),
        first_name=p.get('firstName'),
        last_name=p.get('lastName'),
        primary_number=p.get('primaryNumber'),
        birth_country=p.get('birthCountry'),
        height=p.get('height'),
        weight=p.get('weight'),
        active=p.get('active'),
        current_team_id=p.get('currentTeam').get('id'),
        primary_position_code=p.get('primaryPosition').get('code'),
        primary_position_abbrev=p.get('primaryPosition').get('abbreviation'),
        draft_year=p.get('draftYear'),
        bat_side=p.get('batSide').get('code'),
        pitch_hand=p.get('pitchHand').get('code'),
        strike_zone_top=p.get('strikeZoneTop'),
        strike_zone_bottom=p.get('strikeZoneBottom')
    ) for p in players_raw)
    return players_clean

def teams() -> EntryList[Team]:
    teams_url = "https://statsapi.mlb.com/api/v1/teams"
    teams_raw = get_request_json(teams_url).get('teams')
    teams_clean = EntryList(Team(
        id=t.get('id'),
        name=t.get('name'),
        season=t.get('season'),
        venue_id=t.get('venue', {}).get('id'),
        venue_name=t.get('venue', {}).get('name'),
        team_code=t.get('teamCode'),
        abbreviation=t.get('abbreviation'),
        team_name=t.get('teamName'),
        location_name=t.get('locationName'),
        league_id=t.get('league', {}).get('id'),
        league_name=t.get('league', {}).get('name'),
        division_id=t.get('division', {}).get('id'),
        division_name=t.get('division', {}).get('name'),
        sport_id=t.get('sport', {}).get('id'),
        sport_name=t.get('sport', {}).get('name'),
        parent_org_id=t.get('parentOrgId'),
        parent_org_name=t.get('parentOrgName')
    ) for t in teams_raw)
    return teams_clean

def venues() -> EntryList[Venue]:
    venues_url = "https://ws.statsapi.mlb.com/api/v1/venues?hydrate=fieldInfo,location"
    venues_raw = get_request_json(venues_url).get("venues", [])
    venues_clean = EntryList(
        Venue(
            id=v.get('id'),
            name=v.get('name'),
            turf_type=v.get('fieldInfo', {}).get('turfType'),
            roof_type=v.get('fieldInfo', {}).get('roofType'),
            left_line=v.get('fieldInfo', {}).get('leftLine'),
            left=v.get('fieldInfo', {}).get('left'),
            left_center=v.get('fieldInfo', {}).get('leftCenter'),
            center=v.get('fieldInfo', {}).get('center'),
            right_center=v.get('fieldInfo', {}).get('right_center'),
            right=v.get('fieldInfo', {}).get('right'),
            right_line=v.get('fieldInfo', {}).get('right_line'),
            azimuth_ange=v.get('location', {}).get('azimuthAngle'),
            elevation=v.get('location', {}).get('elevation'),
        ) for v in venues_raw
    )
    return venues_clean

def defense_plays(entity_id: int, start_year: int, end_year: int | None) -> EntryList[DefensePlay]:
    if end_year == None:
        end_year = start_year
    plays_url = "https://baseballsavant.mlb.com/visuals/oaa-data"
    params = {
        'type': 'Fielder',
        'playerId': entity_id,
        'startYear': start_year,
        'endYear': end_year
    }
    plays_raw = get_request_json(plays_url, params)
    plays_clean = EntryList(
        DefensePlay(
            fielder_id=p.get("target_mlb_id"),
            fielder_name=p.get("name_fielder"),
            fielder_team_id=p.get("fld_team_id"),
            fielder_position=p.get("target_id"),
            year=p.get("year"),
            month=p.get("api_game_date_month_mm"),
            est_success=p.get("adj_estimated_success_rate"),
            outs_above_avg=p.get("outs_above_average"),
            runs_prevented=p.get("fielding_runs_prevented"),
            is_out=p.get("is_hit_into_play_field_out")=="1"
        ) for p in plays_raw
    )
    return plays_clean

def gamefeed(game_id: int) -> GamefeedResponse:
    gamefeed_url = f"https://ws.statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
    data = get_request_json(gamefeed_url)
    game_data = data.get("gameData", {})
    game_data_clean = Game(
        id=game_data.get("game", {}).get("pk"),
        type=game_data.get("game", {}).get("type"),
        doubleheader=game_data.get("game", {}).get("doubleheader"),
        season=game_data.get("game", {}).get("season"),
        game_date=game_data.get("datetime", {}).get("officialDate"),
        game_time=game_data.get("datetime", {}).get("time"),
        status_code=game_data.get("status", {}).get("statusCode"),
        home_team_id=game_data.get("teams", {}).get("home", {}).get("id"),
        away_team_id=game_data.get("teams", {}).get("away", {}).get("id"),
        home_team_name=game_data.get("teams", {}).get("home", {}).get("name"),
        away_team_name=game_data.get("teams", {}).get("away", {}).get("name"),
        venue_id=game_data.get("venue", {}).get("id"),
        venue_name=game_data.get("venue", {}).get("name"),
        weather_condition=game_data.get("weather", {}).get("condition"),
        weather_temp=game_data.get("weather", {}).get("temp"),
        weather_wind=game_data.get("weather", {}).get("wind"),
        home_team_pitcher_id=game_data.get("probablePitchers", {}).get("home", {}).get("id"),
        home_team_pitcher_name=game_data.get("probablePitchers", {}).get("home", {}).get("fullName"),
        away_team_pitcher_id=game_data.get("probablePitchers", {}).get("away", {}).get("id"),
        away_team_pitcher_name=game_data.get("probablePitchers", {}).get("away", {}).get("fullName")
    )
    all_plays = data.get("liveData", {}).get("plays", {}).get("allPlays", [])
    pitches = [{'play_data': play, 'pitch_data': pitch} for play in all_plays for pitch in play.get("playEvents", []) if pitch.get('isPitch', False)]
    clean_pitches: EntryList[Pitch] = EntryList()
    for p in pitches:
        play_data = p.get('play_data', {})
        pitch_data = p.get('pitch_data', {})
        home_away_batting = "home" if play_data.get("about", {}).get("halfInning") == "top" else "away"
        home_away_fielding = "away" if home_away_batting == "home" else "home"
        runners = play_data.get("runners", [])
        runner_batter = [runner for runner in runners if runner.get("movement", {}).get("originBase") == None]
        runner_on_1b = [runner for runner in runners if runner.get("movement", {}).get("originBase") == '1B']
        runner_on_2b = [runner for runner in runners if runner.get("movement", {}).get("originBase") == '2B']
        runner_on_3b = [runner for runner in runners if runner.get("movement", {}).get("originBase") == '3B']
        is_runner_on_1b = len(runner_on_1b) > 0
        is_runner_on_2b = len(runner_on_2b) > 0
        is_runner_on_3b = len(runner_on_3b) > 0
        runner_batter_score = runner_batter[0].get("movement", {}).get("end") == "score"  if len(runner_batter) > 0 else False
        runner_1b_score = runner_on_1b[0].get("movement", {}).get("end") == "score" if is_runner_on_1b else False
        runner_2b_score = runner_on_2b[0].get("movement", {}).get("end") == "score" if is_runner_on_2b else False
        runner_3b_score = runner_on_3b[0].get("movement", {}).get("end") == "score" if is_runner_on_3b else False
        clean_pitches.append(Pitch(**{
            "id": pitch_data.get("playId"),
            "inning": play_data.get("about", {}).get("inning"),
            "ab_number": play_data.get("atBatIndex"),
            "batter": play_data.get("matchup", {}).get("batter", {}).get("id"),
            "stand": play_data.get("matchup", {}).get("batSide", {}).get("code"),
            "pitcher": play_data.get("matchup", {}).get("pitcher", {}).get("id"),
            "p_throws": play_data.get("matchup", {}).get("pitchHand", {}).get("code"),
            "team_batting_id": game_data_clean.home_team_id if home_away_batting == "home" else game_data_clean.away_team_id,
            "team_fielding_id": game_data_clean.home_team_id if home_away_fielding == "home" else game_data_clean.away_team_id,
            "result": play_data.get("result", {}).get("event"),
            "events": play_data.get("result", {}).get("event"),
            "strikes": pitch_data.get("count", {}).get("strikes"),
            "balls": pitch_data.get("count", {}).get("balls"),
            "outs": pitch_data.get("count", {}).get("outs"),
            "pitch_type": pitch_data.get("details", {}).get("type", {}).get("code"),
            "call": pitch_data.get("details", {}).get("call", {}).get("description"),
            "pitch_call": pitch_data.get("details", {}).get("call", {}).get("description"),
            "is_strike_swinging": "Swinging Strike" == pitch_data.get("details", {}).get("call", {}).get("description"),
            "start_speed": pitch_data.get("pitchData", {}).get("startSpeed"),
            "extension": pitch_data.get("pitchData", {}).get("extension"),
            "zone": pitch_data.get("pitchData", {}).get("zone"),
            "spin_rate": pitch_data.get("pitchData", {}).get("breaks", {}).get("spinRate"),
            "x0": pitch_data.get("pitchData", {}).get("coordinates", {}).get("x0"),
            "z0": pitch_data.get("pitchData", {}).get("coordinates", {}).get("z0"),
            "breakx": pitch_data.get("pitchData", {}).get("breaks", {}).get("breakHorizontal"),
            "breakz": pitch_data.get("pitchData", {}).get("breaks", {}).get("breakVertical"),
            "inducedbreakz": pitch_data.get("pitchData", {}).get("breaks", {}).get("breakVerticalInduced"),
            "hit_speed": pitch_data.get("hitData", {}).get("launchSpeed"),
            "xba": None,
            "hit_angle": pitch_data.get("hitData", {}).get("launchAngle"),
            "is_barrel": None,
            "pitch_number": pitch_data.get("pitchNumber"),
            "gameid": game_id,
            "px": pitch_data.get("pitchData", {}).get("coordinates", {}).get("pX"),
            "pz": pitch_data.get("pitchData", {}).get("coordinates", {}).get("pZ"),
            "y0": pitch_data.get("pitchData", {}).get("coordinates", {}).get("y0"),
            "ax": pitch_data.get("pitchData", {}).get("coordinates", {}).get("aX"),
            "ay": pitch_data.get("pitchData", {}).get("coordinates", {}).get("aY"),
            "az": pitch_data.get("pitchData", {}).get("coordinates", {}).get("aZ"),
            "vx0": pitch_data.get("pitchData", {}).get("coordinates", {}).get("vX0"),
            "vy0": pitch_data.get("pitchData", {}).get("coordinates", {}).get("vY0"),
            "vz0": pitch_data.get("pitchData", {}).get("coordinates", {}).get("vZ0"),
            "hc_x_ft": pitch_data.get("hitData", {}).get("coordinates", {}).get("coordX"),
            "hc_y_ft": pitch_data.get("hitData", {}).get("coordinates", {}).get("coordY"),
            "runner_on_1b": is_runner_on_1b,
            "runner_on_2b": is_runner_on_2b,
            "runner_on_3b": is_runner_on_3b,
            "runner_batter_score": runner_batter_score,
            "runner_1b_score": runner_1b_score,
            "runner_2b_score": runner_2b_score,
            "runner_3b_score": runner_3b_score,
        }))
    
    # Create boxscore lists
    batter_boxscores: EntryList[BatterBoxscore] = EntryList()
    pitcher_boxscores: EntryList[PitcherBoxscore] = EntryList()
    away_boxscores = list(data.get("liveData", {}).get("boxscore", {}).get("teams", {}).get("away", {}).get("players", {}).values())
    home_boxscores = list(data.get("liveData", {}).get("boxscore", {}).get("teams", {}).get("home", {}).get("players", {}).values())
    boxscores_raw = away_boxscores + home_boxscores
    for boxscore in boxscores_raw:
        batting_boxscore = boxscore.get("stats", {}).get("batting")
        if batting_boxscore:
            boxscore_id = str(game_id) + str(boxscore["person"]["id"])
            batter_boxscores.append(BatterBoxscore(
                id=boxscore_id,
                playerid=boxscore.get("person", {}).get("id"),
                gameid=game_id,
                flyouts=batting_boxscore.get("flyOuts"),
                groundouts=batting_boxscore.get("groundOuts"),
                runs=batting_boxscore.get("runs"),
                homeruns=batting_boxscore.get("homeRuns"),
                strikeouts=batting_boxscore.get("strikeOuts"),
                baseonballs=batting_boxscore.get("baseOnBalls"),
                hits=batting_boxscore.get("hits"),
                atbats=batting_boxscore.get("atBats"),
                caughtstealing=batting_boxscore.get("caughtStealing"),
                stolenbases=batting_boxscore.get("stolenBases"),
                plateappearances=batting_boxscore.get("plateAppearances"),
                rbi=batting_boxscore.get("rbi"),
                doubles=batting_boxscore.get("doubles"),
                triples=batting_boxscore.get("triples"),
                hitbypitch=batting_boxscore.get("hitByPitch"),
            ))
        pitching_boxscore = boxscore.get("stats", {}).get("pitching")
        if pitching_boxscore:
            boxscore_id = str(game_id) + str(boxscore["person"]["id"])
            pitcher_boxscores.append(PitcherBoxscore(
                id=boxscore_id,
                playerid=boxscore.get("person", {}).get("id"),
                gameid=game_id,
                groundouts=pitching_boxscore.get("groundOuts"),
                airouts=pitching_boxscore.get("airOuts"),
                runs=pitching_boxscore.get("runs"),
                strikeouts=pitching_boxscore.get("strikeOuts"),
                baseonballs=pitching_boxscore.get("baseOnBalls"),
                hits=pitching_boxscore.get("hits"),
                hitbypitch=pitching_boxscore.get("hitByPitch"),
                atbats=pitching_boxscore.get("atBats"),
                numberofpitches=pitching_boxscore.get("numberOfPitches"),
                inningspitched=pitching_boxscore.get("inningsPitched"),
                wins=pitching_boxscore.get("wins"),
                losses=pitching_boxscore.get("losses"),
                earnedruns=pitching_boxscore.get("earnedRuns"),
                battersfaced=pitching_boxscore.get("battersFaced"),
                outs=pitching_boxscore.get("outs"),
                balls=pitching_boxscore.get("balls"),
                strikes=pitching_boxscore.get("strikes"),
            ))

    return GamefeedResponse(
        game=game_data_clean,
        pitches=clean_pitches,
        batter_boxscores=batter_boxscores,
        pitcher_boxscores=pitcher_boxscores
    )

