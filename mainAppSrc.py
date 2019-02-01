from utils import utils
import urllib.request

# Handles the items list | A text file with urls separated by ","
strStaticItems = utils.getItemsList("your-urls-list.html")

# Xpath Queries
titleQuery = '//h3/span/text()'
aboutQuery = '//div[@class="about"]//text()'
metaTitleQuery = '//title//text()'
metaDescriptionQuery = '//meta[@name="description"]/@content'
metaKeywordsQuery = '//meta[@name="keywords"]/@content'
tagsQuery = '//ul[@class="widget-tag"]//a//text()'
imagesQuery = '//dt//img//@src'
thumbnailQuery = '//div[@class="item-box"]//img//@src'
thumbnailLinkQuery = '//div[@class="item-box"]//a//@href'

# Counter and Limit for the loop
counter = 0
counter2 = 0
limit = 100

# Getting data
for item in strStaticItems:
    caseUrl = item.strip()
    title = item.split('/')[-1]

    jsonContent = "{"

    if counter < limit:

        # Test if it's a valid content by checking the content title (not the page title)
        contentTitle = utils.getHtmlContent(item.strip(), titleQuery)
        if len(contentTitle) > 0:
            title = ''.join(title)
            cleanTitle = utils.clearTitle(title)

            # Handles cache. If not exists, them create the files
            utils.handleCacheFiles(cleanTitle, caseUrl)

            # Redefines called url after creating cache
            caseUrl = "http://localhost/your-local-app/cache/"+cleanTitle+"/"+cleanTitle+".html"

            # Save images
            imagesList = utils.getHtmlContent(caseUrl, imagesQuery)
            utils.createDir('./cache/'+title+'/media')
            for img in imagesList:
                imageFile = img.split('/')[-1]
                urllib.request.urlretrieve(img, './cache/'+title+'/media/'+imageFile)

            # Insert json data
            jsonContent += utils.xpathToJson(caseUrl, metaTitleQuery, "meta_title")+','
            jsonContent += utils.xpathToJson(caseUrl, metaDescriptionQuery, "meta_description")+','
            jsonContent += utils.xpathToJson(caseUrl, metaKeywordsQuery, "meta_keywords")+','
            jsonContent += utils.xpathToJson(caseUrl, titleQuery, "post_title")+','
            jsonContent += utils.xpathToJson(caseUrl, tagsQuery, "post_tags", ", ")+','

            # Prepare the about content. Could be several <p>
            about = utils.getHtmlContent(caseUrl, aboutQuery)
            allAboutContent = ''
            for aboutContent in about:
                # Convert to string
                aboutContent = ''.join(aboutContent)
                # Put each item wrapped inside <p>
                if len(aboutContent) > 0 and (not aboutContent.isspace()):
                    allAboutContent += '<p>'+aboutContent.strip()+'</p>'

            jsonContent += '\n\t "post_about" : "' + allAboutContent + '"'
            jsonContent += "\n}"

            # Creates a json file for each item
            utils.createFile('./cache/'+title+'/meta.json', jsonContent)
            counter += 1

        continue
    else:
        break


# Save thumbnails
thumbsUrl = "url-where-posts-thumbs-are"
thumbnails = utils.getHtmlContent(thumbsUrl, thumbnailQuery)
thumbnailLink = utils.getHtmlContent(thumbsUrl, thumbnailLinkQuery)

# Align lists due to an inconsistency in HTML structure
del thumbnails[:3]
del thumbnailLink[:3]

for thumbnail in thumbnails:
    if counter2 < limit:
        indexThumb = thumbnails.index(thumbnail)
        myThumbUrl = thumbnailLink[indexThumb].split('/')[-1]
        thumbFile = "featured_"+thumbnail.split('/')[-1]
        urllib.request.urlretrieve(thumbnail, './cache/'+myThumbUrl+'/media/'+thumbFile)
        counter2 += 1
        continue
    else:
        break
