import geocoder

def get_location_info():
    try:
        g = geocoder.ip('me')
        if g.ok:
            return {
                "city": g.city,
                "state": g.state,
                "country": g.country,
                "ip": g.ip,
                "latlng": g.latlng
            }
        else:
            return {"error": "Unable to fetch location"}
    except Exception as e:
        return {"error": str(e)}
