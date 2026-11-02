<?xml version="1.0" encoding="UTF-8"?>
<!--
  Human-readable view of an XML sitemap (urlset or sitemapindex), for browsers only.
  Search engines ignore this file: the sitemap they read is unchanged.

  Install (seo-sitemap skill, Build):
    1. Serve this file from the SAME origin as the sitemap (browsers refuse a cross-origin XSL),
       for example https://example.com/sitemap.xsl, with Content-Type text/xsl or application/xml.
    2. Add on the second line of every sitemap file, right after the XML declaration:
         <?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>
    3. Chrome removes native XSLT on 17 November 2026 (Chrome 158). Without the polyfill, a sitemap
       that calls this stylesheet shows as one block of run-together text. Self-host the official
       polyfill (npm xslt-polyfill, pinned version) next to it and load it as the first child of the
       root element of every sitemap file:
         <script src="/xslt-polyfill.min.js" xmlns="http://www.w3.org/1999/xhtml"></script>
    4. Translate the labels below into the language of the site.

  XSLT 1.0 on purpose: it is the only version browsers (and the xslt-polyfill) run.
-->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
  exclude-result-prefixes="s xhtml image">

  <xsl:output method="html" encoding="UTF-8" indent="no"
    doctype-system="about:legacy-compat"/>

  <!-- Labels: translate these into the language of the site. -->
  <xsl:variable name="t_title">Sitemap</xsl:variable>
  <xsl:variable name="t_index_title">Sitemap index</xsl:variable>
  <xsl:variable name="t_intro">This file lists the pages of the site for search engines and AI assistants. This view is for people; robots read the same file as raw XML.</xsl:variable>
  <xsl:variable name="t_pages">pages</xsl:variable>
  <xsl:variable name="t_files">sitemap files</xsl:variable>
  <xsl:variable name="t_languages">languages</xsl:variable>
  <xsl:variable name="t_sections">Sections</xsl:variable>
  <xsl:variable name="t_page">Page</xsl:variable>
  <xsl:variable name="t_file">Sitemap file</xsl:variable>
  <xsl:variable name="t_alternates">Languages</xsl:variable>
  <xsl:variable name="t_images">Images</xsl:variable>
  <xsl:variable name="t_lastmod">Last updated</xsl:variable>
  <xsl:variable name="t_filter">Filter, for example /blog/ or a word of the address</xsl:variable>
  <xsl:variable name="t_shown">shown</xsl:variable>
  <xsl:variable name="t_all">all</xsl:variable>

  <!-- First path segment of a URL: "https://x.com/en/blog/post" gives "en", the home page gives "". -->
  <xsl:key name="section" match="s:url"
    use="substring-before(concat(substring-after(substring-after(s:loc, '://'), '/'), '/'), '/')"/>
  <xsl:key name="lang" match="xhtml:link[@rel='alternate']" use="@hreflang"/>

  <xsl:variable name="host"
    select="substring-before(concat(substring-after((//s:loc)[1], '://'), '/'), '/')"/>

  <xsl:template match="/">
    <html>
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <meta name="robots" content="noindex"/>
        <title>
          <xsl:choose>
            <xsl:when test="s:sitemapindex"><xsl:value-of select="$t_index_title"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="$t_title"/></xsl:otherwise>
          </xsl:choose>
          <xsl:text>: </xsl:text><xsl:value-of select="$host"/>
        </title>
        <style><![CDATA[
:root{--bg:#f7f7f5;--card:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e6e5e0;--accent:#2f5bea;--chip:#eef1fd;--chip-ink:#2a46b8;--row:#fafaf8}
@media (prefers-color-scheme: dark){:root{--bg:#141413;--card:#1d1d1b;--ink:#ecebe6;--muted:#a3a29b;--line:#33332f;--accent:#8aa6ff;--chip:#24294a;--chip-ink:#c3cfff;--row:#222220}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:32px 16px 64px}
h1{font-size:28px;line-height:1.2;margin:0 0 6px}
.host{color:var(--muted);font-size:15px;margin:0 0 14px}
.intro{color:var(--muted);max-width:760px;margin:0 0 22px}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 22px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 18px;min-width:130px}
.stat b{display:block;font-size:24px;line-height:1.1}
.stat span{color:var(--muted);font-size:13px}
.sections{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 18px}
.sections h2{width:100%;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 2px}
.sec{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:4px 12px;font:inherit;font-size:13px;cursor:pointer}
.sec em{font-style:normal;color:var(--muted);margin-left:6px}
.sec[aria-pressed=true]{border-color:var(--accent);color:var(--accent)}
.filter{width:100%;padding:11px 14px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);font:inherit;margin:0 0 6px}
.count{color:var(--muted);font-size:13px;margin:0 0 12px}
.table{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
table{width:100%;border-collapse:collapse;font-size:inherit;font-family:inherit;color:inherit}
th{text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);padding:10px 14px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--card)}
td{padding:9px 14px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--row)}
td.n{color:var(--muted);font-variant-numeric:tabular-nums;width:1%;white-space:nowrap}
td.d{white-space:nowrap;color:var(--muted);font-variant-numeric:tabular-nums;width:1%}
td.i{width:1%;text-align:center;color:var(--muted)}
a{color:var(--accent);text-decoration:none;word-break:break-all}
a:hover{text-decoration:underline}
.chips{display:flex;flex-wrap:wrap;gap:4px}
.chip{background:var(--chip);color:var(--chip-ink);border-radius:6px;padding:1px 7px;font-size:12px;word-break:normal}
.chip.x{background:transparent;border:1px solid var(--line);color:var(--muted)}
@media (max-width:720px){th.l,td.l,th.i,td.i{display:none}h1{font-size:23px}}
        ]]></style>
      </head>
      <body>
        <div class="wrap">
          <xsl:apply-templates/>
        </div>
        <script><![CDATA[
(function(){
  var input=document.getElementById('q'); if(!input) return;
  var rows=[].slice.call(document.querySelectorAll('tbody tr'));
  var out=document.getElementById('shown');
  var chips=[].slice.call(document.querySelectorAll('.sec'));
  rows.forEach(function(r){var p=r.getAttribute('data-p')||'/'; if(p.slice(-1)!=='/') p+='/'; r.setAttribute('data-p',p);});
  function run(){
    var q=input.value.trim().toLowerCase(), n=0;
    rows.forEach(function(r){var hit=!q||r.getAttribute('data-p').toLowerCase().indexOf(q)!==-1||r.textContent.toLowerCase().indexOf(q)!==-1; r.style.display=hit?'':'none'; if(hit) n++;});
    if(out) out.textContent=n;
    chips.forEach(function(c){c.setAttribute('aria-pressed', String((c.getAttribute('data-q')||'')===q));});
  }
  input.addEventListener('input',run);
  chips.forEach(function(c){c.addEventListener('click',function(){input.value=c.getAttribute('data-q')||''; run(); input.focus();});});
})();
        ]]></script>
      </body>
    </html>
  </xsl:template>

  <!-- Sitemap index: the list of child sitemap files. -->
  <xsl:template match="s:sitemapindex">
    <h1><xsl:value-of select="$t_index_title"/></h1>
    <p class="host"><xsl:value-of select="$host"/></p>
    <p class="intro"><xsl:value-of select="$t_intro"/></p>
    <div class="stats">
      <div class="stat"><b><xsl:value-of select="count(s:sitemap)"/></b><span><xsl:value-of select="$t_files"/></span></div>
    </div>
    <div class="table">
      <table>
        <thead><tr><th>#</th><th><xsl:value-of select="$t_file"/></th><th><xsl:value-of select="$t_lastmod"/></th></tr></thead>
        <tbody>
          <xsl:for-each select="s:sitemap">
            <tr>
              <td class="n"><xsl:value-of select="position()"/></td>
              <td><a href="{s:loc}"><xsl:value-of select="s:loc"/></a></td>
              <td class="d"><xsl:value-of select="substring(s:lastmod, 1, 10)"/></td>
            </tr>
          </xsl:for-each>
        </tbody>
      </table>
    </div>
  </xsl:template>

  <!-- Sitemap of pages. -->
  <xsl:template match="s:urlset">
    <xsl:variable name="langs" select="//xhtml:link[@rel='alternate'][generate-id() = generate-id(key('lang', @hreflang)[1])][@hreflang != 'x-default']"/>
    <xsl:variable name="hasImages" select="boolean(//image:image)"/>
    <h1><xsl:value-of select="$t_title"/></h1>
    <p class="host"><xsl:value-of select="$host"/></p>
    <p class="intro"><xsl:value-of select="$t_intro"/></p>
    <div class="stats">
      <div class="stat"><b><xsl:value-of select="count(s:url)"/></b><span><xsl:value-of select="$t_pages"/></span></div>
      <xsl:if test="count($langs) &gt; 1">
        <div class="stat"><b><xsl:value-of select="count($langs)"/></b><span><xsl:value-of select="$t_languages"/></span></div>
      </xsl:if>
    </div>

    <div class="sections">
      <h2><xsl:value-of select="$t_sections"/></h2>
      <button class="sec" type="button" data-q="" aria-pressed="true"><xsl:value-of select="$t_all"/><em><xsl:value-of select="count(s:url)"/></em></button>
      <xsl:for-each select="s:url[generate-id() = generate-id(key('section', substring-before(concat(substring-after(substring-after(s:loc, '://'), '/'), '/'), '/'))[1])]">
        <xsl:sort select="count(key('section', substring-before(concat(substring-after(substring-after(s:loc, '://'), '/'), '/'), '/')))" data-type="number" order="descending"/>
        <xsl:variable name="seg" select="substring-before(concat(substring-after(substring-after(s:loc, '://'), '/'), '/'), '/')"/>
        <!-- A section is a folder holding at least 2 pages; single pages stay in the table. -->
        <xsl:if test="$seg != '' and count(key('section', $seg)) &gt; 1">
          <button class="sec" type="button" data-q="/{$seg}/">
            <xsl:value-of select="$seg"/>
            <em><xsl:value-of select="count(key('section', $seg))"/></em>
          </button>
        </xsl:if>
      </xsl:for-each>
    </div>

    <input id="q" class="filter" type="search" placeholder="{$t_filter}" aria-label="{$t_filter}"/>
    <p class="count"><span id="shown"><xsl:value-of select="count(s:url)"/></span> / <xsl:value-of select="count(s:url)"/><xsl:text> </xsl:text><xsl:value-of select="$t_pages"/><xsl:text> </xsl:text><xsl:value-of select="$t_shown"/></p>

    <div class="table">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th><xsl:value-of select="$t_page"/></th>
            <xsl:if test="count($langs) &gt; 1"><th class="l"><xsl:value-of select="$t_alternates"/></th></xsl:if>
            <xsl:if test="$hasImages"><th class="i"><xsl:value-of select="$t_images"/></th></xsl:if>
            <th><xsl:value-of select="$t_lastmod"/></th>
          </tr>
        </thead>
        <tbody>
          <xsl:for-each select="s:url">
            <xsl:variable name="path" select="concat('/', substring-after(substring-after(s:loc, '://'), '/'))"/>
            <tr data-p="{$path}">
              <td class="n"><xsl:value-of select="position()"/></td>
              <td><a href="{s:loc}"><xsl:value-of select="$path"/></a></td>
              <xsl:if test="count($langs) &gt; 1">
                <td class="l">
                  <span class="chips">
                    <xsl:for-each select="xhtml:link[@rel='alternate']">
                      <a href="{@href}">
                        <xsl:attribute name="class">
                          <xsl:choose>
                            <xsl:when test="@hreflang = 'x-default'">chip x</xsl:when>
                            <xsl:otherwise>chip</xsl:otherwise>
                          </xsl:choose>
                        </xsl:attribute>
                        <xsl:value-of select="@hreflang"/>
                      </a>
                    </xsl:for-each>
                  </span>
                </td>
              </xsl:if>
              <xsl:if test="$hasImages"><td class="i"><xsl:value-of select="count(image:image)"/></td></xsl:if>
              <td class="d"><xsl:value-of select="substring(s:lastmod, 1, 10)"/></td>
            </tr>
          </xsl:for-each>
        </tbody>
      </table>
    </div>
  </xsl:template>
</xsl:stylesheet>
