import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom

TOKEN = 'GITHUB_TOKEN'

# GitHub API for listing repositories
API_URL = 'https://api.github.com/user/repos'

def fetch_github_repos():
    """Fetch the list of repositories for the authenticated user."""
    headers = {'Authorization': f'token {TOKEN}'}
    params = {'affiliation': 'owner,collaborator,organization_member', 'per_page': 100}
    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def create_manifest(repos):
    """Generate manifest file from the list of repositories."""
    manifest = ET.Element('manifest')
    remote = ET.SubElement(manifest, 'remote', review='https://github.com/')
    
    for repo in repos:
        path = repo['name']
        name = repo['full_name']
        ET.SubElement(manifest, 'project', path=path, name=name)

    # Convert the XML element tree to a string and pretty-print it
    rough_string = ET.tostring(manifest, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def save_manifest(manifest, filename='manifest.xml'):
    """Save the manifest XML string to a file."""
    with open(filename, 'w') as f:
        f.write(manifest)

def main():
    repos = fetch_github_repos()
    manifest = create_manifest(repos)
    save_manifest(manifest)
    print(f'Manifest file has been saved as "manifest.xml".')

if __name__ == '__main__':
    main()

    
