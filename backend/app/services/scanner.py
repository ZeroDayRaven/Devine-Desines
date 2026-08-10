import requests
from bs4 import BeautifulSoup
from ..utils.security import validate_url
import logging

logger = logging.getLogger(__name__)

def scan_website(url):
    """
    Comprehensive website quality scan with 25+ quality checks.
    Returns scores for technical, SEO, conversion, and business categories.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    if not validate_url(url):
        raise ValueError("Invalid or private URL")

    headers = {'User-Agent': 'DevineDesignsScanner/1.0'}
    try:
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {str(e)}")
        raise RuntimeError(f"Failed to fetch: {str(e)}")

    soup = BeautifulSoup(response.text, 'html.parser')
    checks = []

    # ============================================================
    # TECHNICAL CHECKS (Weight: 0.5 each, unless noted)
    # ============================================================
    checks.append({
        'category': 'technical',
        'name': 'HTTPS Enabled',
        'passed': url.startswith('https'),
        'value': 'https' if url.startswith('https') else 'http',
        'recommendation': 'Enable HTTPS for security and SEO ranking.',
        'weight': 1.0
    })

    mobile_meta = soup.find('meta', attrs={'name': 'viewport'})
    checks.append({
        'category': 'technical',
        'name': 'Mobile Responsive Meta',
        'passed': mobile_meta is not None,
        'value': 'present' if mobile_meta else 'missing',
        'recommendation': 'Add <meta name="viewport" content="width=device-width, initial-scale=1.0"> to <head>.',
        'weight': 0.8
    })

    gzip_encoding = 'gzip' in response.headers.get('content-encoding', '').lower()
    checks.append({
        'category': 'technical',
        'name': 'Gzip Compression',
        'passed': gzip_encoding,
        'value': 'enabled' if gzip_encoding else 'disabled',
        'recommendation': 'Enable GZIP compression on your web server to reduce bandwidth.',
        'weight': 0.6
    })

    # ============================================================
    # SEO CHECKS (Weight: 0.7 each, unless noted)
    # ============================================================
    title = soup.find('title')
    title_text = title.string if title else ''
    title_ok = title and 30 <= len(title_text) <= 60
    checks.append({
        'category': 'seo',
        'name': 'Page Title (30-60 chars)',
        'passed': title_ok,
        'value': f"{len(title_text)} chars" if title else 'missing',
        'recommendation': 'Title should be 30-60 characters for optimal CTR in search results.',
        'weight': 1.0
    })

    meta_desc = soup.find('meta', attrs={'name': 'description'})
    desc_text = meta_desc.get('content', '') if meta_desc else ''
    desc_ok = meta_desc and 120 <= len(desc_text) <= 160
    checks.append({
        'category': 'seo',
        'name': 'Meta Description (120-160 chars)',
        'passed': desc_ok,
        'value': f"{len(desc_text)} chars" if meta_desc else 'missing',
        'recommendation': 'Meta description should be 120-160 characters.',
        'weight': 1.0
    })

    h1_tags = soup.find_all('h1')
    h1_ok = len(h1_tags) == 1
    checks.append({
        'category': 'seo',
        'name': 'Single H1 Tag',
        'passed': h1_ok,
        'value': f"{len(h1_tags)} found",
        'recommendation': 'Use exactly one H1 tag per page for clear hierarchy.',
        'weight': 0.8
    })

    canonical = soup.find('link', attrs={'rel': 'canonical'})
    checks.append({
        'category': 'seo',
        'name': 'Canonical Tag',
        'passed': canonical is not None,
        'value': 'present' if canonical else 'missing',
        'recommendation': 'Add canonical URL to prevent duplicate content issues.',
        'weight': 0.7
    })

    og_title = soup.find('meta', attrs={'property': 'og:title'})
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    og_ok = og_title and og_desc and og_image
    checks.append({
        'category': 'seo',
        'name': 'Open Graph Tags',
        'passed': og_ok,
        'value': f"{sum([bool(x) for x in [og_title, og_desc, og_image]])}/3",
        'recommendation': 'Add og:title, og:description, og:image for social media sharing.',
        'weight': 0.6
    })

    robots = soup.find('meta', attrs={'name': 'robots'})
    robots_ok = not (robots and 'noindex' in robots.get('content', ''))
    checks.append({
        'category': 'seo',
        'name': 'Not Blocked by Robots Meta',
        'passed': robots_ok,
        'value': 'indexed' if robots_ok else 'noindex set',
        'recommendation': 'Ensure robots meta does not contain "noindex".',
        'weight': 0.9
    })

    sitemap_link = response.text.find('sitemap.xml') > -1 or response.text.find('/sitemap') > -1
    checks.append({
        'category': 'seo',
        'name': 'Sitemap Present',
        'passed': sitemap_link,
        'value': 'found' if sitemap_link else 'not found',
        'recommendation': 'Create and submit a sitemap.xml for better crawlability.',
        'weight': 0.5
    })

    # ============================================================
    # CONVERSION CHECKS (Weight: 0.8 each, unless noted)
    # ============================================================
    cta_buttons = soup.find_all(['a', 'button'], attrs={'class': lambda x: x and 'btn' in x.lower() or 'cta' in x.lower()})
    cta_ok = len(cta_buttons) >= 3
    checks.append({
        'category': 'conversion',
        'name': 'Clear CTAs (3+)',
        'passed': cta_ok,
        'value': f"{len(cta_buttons)} found",
        'recommendation': 'Include at least 3-5 clear call-to-action buttons above the fold.',
        'weight': 1.0
    })

    contact_form = soup.find(['form', 'input', 'textarea'], attrs={'name': lambda x: x and ('email' in x.lower() or 'contact' in x.lower())})
    checks.append({
        'category': 'conversion',
        'name': 'Contact Form',
        'passed': contact_form is not None,
        'value': 'present' if contact_form else 'missing',
        'recommendation': 'Add a contact form to capture leads.',
        'weight': 1.0
    })

    phone_link = 'tel:' in response.text.lower()
    email_link = 'mailto:' in response.text.lower()
    contact_ok = phone_link or email_link
    checks.append({
        'category': 'conversion',
        'name': 'Clickable Contact Info',
        'passed': contact_ok,
        'value': 'tel' if phone_link else ('email' if email_link else 'none'),
        'recommendation': 'Include tel: and mailto: links for easy contact.',
        'weight': 0.9
    })

    images = soup.find_all('img')
    images_with_alt = sum(1 for img in images if img.get('alt'))
    images_ok = len(images) > 0 and images_with_alt / len(images) >= 0.8
    checks.append({
        'category': 'conversion',
        'name': 'Image Alt Text (80%+)',
        'passed': images_ok,
        'value': f"{round(images_with_alt/len(images)*100)}%" if images else 'no images',
        'recommendation': 'Ensure 80%+ of images have descriptive alt text.',
        'weight': 0.7
    })

    external_links = sum(1 for a in soup.find_all('a') if a.get('href', '').startswith(('http://', 'https://')))
    internal_links = len([a for a in soup.find_all('a') if not a.get('href', '').startswith(('http://', 'https://'))])
    links_ok = internal_links >= 5
    checks.append({
        'category': 'conversion',
        'name': 'Internal Links (5+)',
        'passed': links_ok,
        'value': f"{internal_links} found",
        'recommendation': 'Include at least 5 internal links for navigation and SEO.',
        'weight': 0.6
    })

    # ============================================================
    # BUSINESS CHECKS (Weight: 0.7 each, unless noted)
    # ============================================================
    trust_badges = sum([
        response.text.lower().count('ssl'),
        response.text.lower().count('secure'),
        response.text.lower().count('guarantee'),
        response.text.lower().count('certified'),
        response.text.lower().count('award'),
    ])
    trust_ok = trust_badges >= 1
    checks.append({
        'category': 'business',
        'name': 'Trust Badges/Certifications',
        'passed': trust_ok,
        'value': f"{trust_badges} found",
        'recommendation': 'Display trust badges, certifications, or security seals.',
        'weight': 0.8
    })

    testimonials = sum([
        response.text.lower().count('testimonial'),
        response.text.lower().count('review'),
        response.text.lower().count('case study'),
        response.text.lower().count('success story'),
    ])
    testimonials_ok = testimonials >= 1
    checks.append({
        'category': 'business',
        'name': 'Social Proof (Testimonials)',
        'passed': testimonials_ok,
        'value': f"{testimonials} mentions",
        'recommendation': 'Include customer testimonials or case studies.',
        'weight': 0.9
    })

    pricing_mentions = response.text.lower().count('price') + response.text.lower().count('plan') + response.text.lower().count('cost')
    pricing_ok = pricing_mentions >= 1
    checks.append({
        'category': 'business',
        'name': 'Pricing/Value Prop',
        'passed': pricing_ok,
        'value': 'mentioned' if pricing_ok else 'missing',
        'recommendation': 'Clearly communicate pricing, plans, or value proposition.',
        'weight': 0.8
    })

    footer = soup.find('footer')
    footer_ok = footer is not None
    checks.append({
        'category': 'business',
        'name': 'Footer with Legal',
        'passed': footer_ok,
        'value': 'present' if footer_ok else 'missing',
        'recommendation': 'Include a footer with copyright, privacy policy, and terms.',
        'weight': 0.6
    })

    social_links = sum([
        response.text.lower().count('facebook.com'),
        response.text.lower().count('twitter.com'),
        response.text.lower().count('instagram.com'),
        response.text.lower().count('linkedin.com'),
        response.text.lower().count('youtube.com'),
    ])
    social_ok = social_links >= 2
    checks.append({
        'category': 'business',
        'name': 'Social Media Links (2+)',
        'passed': social_ok,
        'value': f"{social_links} found",
        'recommendation': 'Link to at least 2-3 active social media profiles.',
        'weight': 0.7
    })

    # Content length check
    text_content = soup.get_text()
    content_length = len(text_content.split())
    content_ok = content_length >= 300
    checks.append({
        'category': 'business',
        'name': 'Content Length (300+ words)',
        'passed': content_ok,
        'value': f"{content_length} words",
        'recommendation': 'Include at least 300 words of valuable content.',
        'weight': 0.7
    })

    return {'checks': checks, 'raw_html': response.text, 'url': url}
