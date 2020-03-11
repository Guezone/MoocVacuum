from selenium import webdriver
import time, io, os, re, requests, pypandoc, shutil
from bs4 import BeautifulSoup as bs
prec_title = ""

# Lauch the script 
print("")
print("--------------------------------------------------------------------")
print("						Welcome to MoocVacuum	(by Guezone)	   ")
print("--------------------------------------------------------------------")
print("")
connect_url = input("# Enter the URL of the website to be vacuumed : ")
time.sleep(2)
content_id = input("# Enter the HTML ID where the content is located  : ")
nextbutton_id = input ("# Enter the HTML ID of the NEXT PAGE button : ")
print("WHEN LAUNCHING THE BROWSER YOU HAVE 1 MINUTE TO AUTHENTICATE YOURSELF OR ACCESS THE DESIRED COURSE")
time.sleep(4)

# Lanch Chrome web driver 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(chrome_options=options)
driver.get(connect_url)
time.sleep(45)
# Write the begin of HTML output file
begin = '<!DOCTYPE html><html><head><title>Like</title><meta content="text/html;charset=utf-8" http-equiv="Content-Type"></head><body>'
end = '</body></html>'
filename = "doc.html"
file = open(filename, "w")
file.write(begin)
file.close()
exit = False
img_count = 0
old_url = ""
# Create directory for images downloaded on the MOOC
if os.path.isdir("./Images") == False:
	os.mkdir("./Images")
# Browse all of Mooc pages
while exit == False :
	# Check if the page has not already been vacuumed, exit script if is a last page
	current_url = str(driver.current_url)
	if current_url == old_url : 
		exit = True
	# Vacuum HTML source code
	code = driver.page_source
	# Keep only course content through DIV ID
	soup  = bs(code,'html.parser') 
	html_content = soup.find("div", {"id" : "forScroll"})
	# Get images html identifier
	img_tags = soup.findAll('img')
	# Browse all of images html identifier for get URL
	for img in img_tags:
	# Get URL of image
		img_url = str(img.get('src'))
		# Set random filename 
		if ".png" in img_url:
			img_count += 1 
			img_filename = str(img_count)+".png"
		if ".jpg" or ".jpeg" in img_url:
			img_count += 1 
			img_filename = str(img_count)+".jpg"
		if ".tif" in img_url:
			img_count += 1 
			img_filename = str(img_count)+".tif"
		# Get full URL of pictures
		if "http" in img_url:
			img_DLurl = img_url
			continue
		else:
			img_DLurl = img_url.replace("../download",site+"download")
		try:
			# Download pitcure
			img_data = requests.get(img_DLurl).content
			# Write file of picture
			with open("./Images/"+img_filename, 'wb') as handler:
				handler.write(img_data)
		except:
			pass
		
		# Replace src attribute in html code
		img_url = str(img_url)
		html_content = str(html_content)
		html_content = html_content.replace(img_url,"./Images/"+img_filename)
		
	# Minimize title
	html_content = html_content.replace("h3","h4")
	html_content = html_content.replace("h2","h3")
	html_content = html_content.replace("h1","h2")
	# Get title of chapter and add it on content
	summary_code = str(soup.find("li", {"class" : "Opened Current"}))	
	titlecode  = bs(summary_code,'html.parser') 
	main_title = str(titlecode.find('h2'))
	main_title = main_title.replace("h2","h1")
	if main_title != prec_title:
		html_content = main_title + html_content
	prec_title = main_title

	# Write on HTML output file 
	with io.open(filename, "a", encoding="utf-8") as f:
		f.write(str(html_content))
	time.sleep(1)

	# Go to the next page using the "NEXT" button ID
	old_url = str(driver.current_url)
	driver.find_element_by_id(nextbutton_id).click()
	time.sleep(1)

# Writes HTML tags for end of files
file = open(filename, "a")
file.write(end)
file.close()
print("--------------------------------------------------------------------")
print("		 HTML BOOK IS EXTRACT... Now convert to .DOCX file... ")
print("--------------------------------------------------------------------")
# Convert HTML Book to .DOCX file
output = pypandoc.convert(source='./doc.html', format='html', to='docx', outputfile='MyBook.docx', extra_args=['-RTS'])
# Clean up folder 
shutil.rmtree("./Images")# print("")
os.remove("doc.html")
