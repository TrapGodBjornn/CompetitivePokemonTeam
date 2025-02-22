import os

template_path = os.path.join('templates', 'index.html')
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print("File contains 'The Battle Lab':", 'The Battle Lab' in content)
    print("File contains 'Bjorn's Battle Assistant':", "Bjorn's Battle Assistant" in content)
    
    # Print the banner section
    start = content.find('<div class="banner">')
    end = content.find('</div>', start)
    print("\nBanner section:")
    print(content[start:end+6]) 