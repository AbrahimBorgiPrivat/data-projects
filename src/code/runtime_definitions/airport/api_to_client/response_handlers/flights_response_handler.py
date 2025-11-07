def response_handler(resp):
    flights = resp.get("departures", [])
    return [
        {
            "flight_number": f.get("number"),
            "scheduled_utc": f.get("movement", {}).get("scheduledTime", {}).get("utc"),
            "airline": f.get("airline", {}).get("name"),
            "airline_iata": f.get("airline", {}).get("iata"),
            "airline_icao": f.get("movement", {}).get("airport", {}).get("icao"),
            "destination": f.get("movement", {}).get("airport", {}).get("name"),
            "destination_iata": f.get("movement", {}).get("airport", {}).get("iata"),
            "destination_icao": f.get("movement", {}).get("airport", {}).get("icao"),
            "scheduled_local": f.get("movement", {}).get("scheduledTime", {}).get("local"),
            "revised_utc": f.get("movement", {}).get("revisedTime", {}).get("utc"),
            "revised_local": f.get("movement", {}).get("revisedTime", {}).get("local"),
            "runway_utc": f.get("movement", {}).get("runwayTime", {}).get("utc"), 
            "runway_local": f.get("movement", {}).get("runwayTime", {}).get("local"), 
            "status": f.get("status"),
            "terminal": f.get("movement", {}).get("terminal"),
            "gate": f.get("movement", {}).get("gate"),
            "aircraft_model": f.get("aircraft", {}).get("model"),
            "aircraft_reg": f.get("aircraft", {}).get("reg"),
        }
        for f in flights
    ]
