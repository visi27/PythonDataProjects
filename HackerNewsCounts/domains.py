from read import load_data

def extract_domain(subdomain):
    if len(str(subdomain).split('.')) > 2:
        return '.'.join(str(subdomain).split('.')[1:])
    return subdomain
 
data = load_data()
data['url'] = data['url'].apply(extract_domain)
domain_counts = data["url"].value_counts()

print(domain_counts[:100])