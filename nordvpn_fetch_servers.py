import requests

def get_country_id(country_name):
    """
    Fetches the list of countries and finds the ID for the given country name.
    """
    url = "https://api.nordvpn.com/v1/servers/countries"
    response = requests.get(url)
    response.raise_for_status()
    
    countries = response.json()
    for country in countries:
        if country["name"].lower() == country_name.lower():
            return country["id"]
    return None

def get_servers_by_country_id(country_id):
    """
    Fetches the server list for a specific country ID.
    """
    url = f"https://api.nordvpn.com/v1/servers?filters[country_id]={country_id}"
    response = requests.get(url)
    response.raise_for_status()
    
    servers = response.json()
    server_details = []
    for server in servers:
        hostname = server.get("hostname")
        ip_address = server.get("station")
        public_key = None
        for tech in server.get("technologies", []):
            for meta in tech.get("metadata", []):
                if meta.get("name") == "public_key":
                    public_key = meta.get("value")
        if hostname and ip_address and public_key:
            server_details.append({
                "hostname": hostname,
                "ip_address": ip_address,
                "public_key": public_key
            })
    return server_details

def main():
    country_name = input("Enter the country name: ").strip()
    country_id = get_country_id(country_name)
    
    if not country_id:
        print(f"Country '{country_name}' not found.")
        return

    print(f"Fetching servers for {country_name} (ID: {country_id})...")
    servers = get_servers_by_country_id(country_id)
    
    if servers:
        print(f"Found {len(servers)} servers in {country_name}:")
        for server in servers:
            print(f"- Hostname: {server['hostname']}")
            print(f"  IP Address: {server['ip_address']}")
            print(f"  Public Key: {server['public_key']}")
            print()
    else:
        print(f"No servers found for {country_name}.")

if __name__ == "__main__":
    main()

