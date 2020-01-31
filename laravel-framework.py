import os, random
#to get pymy.py file please README to get the download url
from pymy import *
from glob import iglob
from bs4 import BeautifulSoup as bs
from shutil import move
import time
import threading

stopprocess = ''

class BuildLaravelBackEnd():
	global stopprocess

	def __init__(self):
		#Path where the website folder is
		self.pathfile = r'C:\xampp\htdocs\eurojack'
		#folder name where converter site will be saved to
		self.build_folder = '_laravelbuild'
		#exclude folders names seperate with comma if any.
		#this exclude folders will not be rename from .php to .blade.php if folder is specified will be ignored
		self.exfolder = []
		#global url for SEO friendly parsing such as {{url}} to be replaced with http://yoursite.com
		self.global_shorten_laravelurl = '{{url}}'
		## PLEASE DO NOT CHANGE FILES BELOW
		self.laravel_image = 'public/images'
		self.laravel_font = 'public/fonts'
		#self.laravel_other = 'public/unknown'
		self.laravel_scss = 'resources/scss'
		self.laravel_js = 'resources/js'
		self.laravel_view = 'resources/view'
		# this are folders and file to allow processing
		self.css_list = ['.css', '.scss']
		self.java_list = ['.js', '.java', '.tf', '.json']
		self.extension_list = ['.php', '.htm', '.html', '.py', '.css', '.scss', '.js', '.inc', '.asp', '.xml']
		#this will skip all folders with this names by not recreating them because laravel has it own
		#specified framework structure so we follow the structures
		self.skip_folder_create_list = ['images', 'css', 'js', 'img', 'fonts', 'scss']
		#this are media files to move and save to images folder
		self.media_list = ['.png', '.jpg', '.jpeg', '.fla', '.swf', '.gif', '.cur', '.ico', '.icon', '.mov', '.mp3', '.mp4', '.avi', '.mpeg', '.pdf', '.doc','.docx', '.svg']
		#this are fonts files to move and save to fonts folder
		self.font_list = ['.ttf', '.woff', '.woff2', '.wof', '.eot', '.less', '.otf', '.ac']
		#this are only allowed files to process
		self.allow_list = ['.php', '.htm', '.html', '.py', '.asp', '.xml']
		passdata = dict()
		passdata['js'] = self.laravel_js
		passdata['css'] = self.laravel_scss
		passdata['img'] = self.laravel_image
		passdata['font'] = self.laravel_font
		#passdata['others'] = self.laravel_other
		passdata['view'] = self.laravel_view

		## END DO NOT CHANGED FILES

		if os.path.exists(self.pathfile):
			print('::PARSED STARTED.....\n============================================================\n')
			for prefolders in passdata:
				#create all folders
				makefolder(joinpath(self.build_folder,  passdata[prefolders]))

			log('::PARSED STARTED.....\n============================================================\n', self.build_folder, '_Log.txt')
			passdata['log'] = self.build_folder
			passdata['div_stype'] = self.build_folder

			if os.path.isdir(self.pathfile):
				for foundfile in iglob(joinpath(self.pathfile, "**/*"), recursive=True):
					if stopprocess:
						print( '\n....Oop USER ABORTED THE PARSING.....')
						break

					normalfoundfile = normalpath(foundfile)
					normalPathfile = normalpath(self.pathfile)
					foundlocal_path = normalfoundfile.replace(normalPathfile, '')
					usefoundlocal_path = urlfolder(foundlocal_path)
					newpath = normalfoundfile

					targetfolder = joinpath(self.build_folder, self.laravel_view)
					usefolder = joinpath(targetfolder, usefoundlocal_path)

					foundfile_basename = basename(foundfile)
					foundfile_first_foldername = firstpath_name(newpath)
					passdata['mainpath'] = firstfolder(foundfile)

					if os.path.isdir(foundfile):
						if not foundfile_basename in self.skip_folder_create_list:
							if not foundfile_first_foldername in self.skip_folder_create_list:
								makefolder(usefolder)
								print( ' ->Folder ' +usefoundlocal_path + ' created..')

					if os.path.isfile(foundfile):
						passdata['build'] = usefolder
						passdata['filename'] = foundfile
						print( '->Parsing ' + joinpath(newpath, foundfile_basename) + ' started..')
						self.file_parser(passdata)
					# time.sleep(0.2)

			log('README \n=======================================\n1. NOTE: 2 main folders are create [PUBLIC] and [RESOURCES] which has 5 default folders /view, /js, /css, /images, /fonts\n2. All php files were rename to blade while all css were rename to scss and stored at resources/view\n3. This folders store all extension to their described folders and automatically correct all link pointing to each folders associated with his extensions\n\n. Thanks for using this software \nYou can contact us directly wemediaent@gmail.com for more suggestions or complaints\nWe are working to include more functions', self.build_folder, '_README.txt')

			movetofolder = joinpath(firstfolder(self.pathfile), self.build_folder)
			if not os.path.exists(movetofolder):
				move(self.build_folder, movetofolder)
				pass
			else:
				from random import randrange
				move(self.build_folder, movetofolder +'_' + str(randrange(0, 1000)))
				pass
			print( 'PARSED COMPLETED')

	def copyDependancy(self, passdata):
		parsefile = passdata['filename']
		parsefile_ext = exts(parsefile).lower()
		parsed_filebasename = basename(parsefile)
		base = os.path.splitext(parsed_filebasename)[0]
		js_folder = joinpath(self.build_folder, self.laravel_js)
		css_folder = joinpath(self.build_folder, self.laravel_scss)
		img_folder = joinpath(self.build_folder, self.laravel_image)
		font_folder = joinpath(self.build_folder, self.laravel_font)
		#others_folder = joinpath(self.build_folder, self.laravel_other)
		log_folder = passdata['log']
		app = ''
		appfile = ''
		appfolder = ''

		if parsefile_ext in self.css_list:
			#remove any trailing _
			base = base.replace('_', '')
			app = "@import '" + base + "';"
			appfile = 'app.scss'
			appfolder = css_folder
			copy_dependancy_file = joinpath(css_folder, '_' + base + '.scss')

		elif parsefile_ext in self.font_list:
			copy_dependancy_file = joinpath(font_folder, parsed_filebasename)

		elif parsefile_ext in self.java_list:
			app = "require('./" + base + "');"
			appfile = 'app.js'
			appfolder = js_folder
			copy_dependancy_file = joinpath(js_folder, parsed_filebasename)

		else:
			copy_dependancy_file = joinpath(img_folder, parsed_filebasename)

		try:
			if not os.path.exists(copy_dependancy_file):
				if appfile:
					css_js_content = parse_css_js(parsefile, 'images')
					log(css_js_content, appfolder, basename(copy_dependancy_file))
					log(app + '\n', appfolder, appfile)
				else:
					copyfiles(parsefile, copy_dependancy_file)
				print( ' ->Copied DEPENDENCY FILE: ' + parsed_filebasename)

		except Exception as e:
			print( ' ->Copying dependancy Error: ' + str(e))
			log('\nCopying dependancy Error occured: ' +str(e), log_folder, '_Log.txt')

	def parser(self, passdata):
		result = ''
		excludefolder = self.exfolder
		parsefile = passdata['filename']
		laravel_url = self.global_shorten_laravelurl
		path_dir = passdata['build']
		js_folder = 'js'
		css_folder = 'css'
		img_folder = 'images'
		font_folder = 'fonts'
		others_folder = img_folder
		log_folder = passdata['log']
		write_parsed_file_to = basename(parsefile)
		parsefile_ext = exts(write_parsed_file_to)
		basenames = os.path.splitext(write_parsed_file_to)[0]

		if parsefile_ext == '.php':
			# overwrite name if php to rename it to blade
			if not '*' in excludefolder:
				# this will exclude all folders and files from auto renaming file to .blade extension
				excludefolder_basename = basename(passdata['mainpath'])
				if not excludefolder_basename in excludefolder:
					write_parsed_file_to = basenames + '.blade.php'

		countimg = 0
		counta = 0
		countlink = 0
		countjs = 0
		counts = 0

		try:
			try:
				# firstly read the file and process all URL from DIV Style background-image: URl()
				html_content = parse_css_js(parsefile, img_folder, laravel_url)
			except Exception:
				html_content = localread_file(parsefile)

			soup = bs(html_content, 'html.parser')

			a_result = '\n<A HREF> parsed started for: ' + parsefile + '\n'
			print( ' -><A HREF> parsed started for: ' + parsefile)
			a_result += '===================================================================\n'
			print(' ->===================================================================')

			try:
				for atag in soup.find_all('a'):
					a_href = atag['href']
					log_ = laravel_url + new_urlpath(a_href)
					atag['href'] = log_
					counta += 1
					a_result += 'OLD href: ' + a_href + ' NEW href: ' + log_ + '\n'
					print(' ->OLD href: ' + a_href + ' NEW href: ' + log_)

				a_result += str(counta) +  ' <a href> was found and processed END\n\n'
				print( ' ->'+str(counta) + ' <a href> was found and processed END')

				if counta > 0:
					log(a_result, log_folder, '_Log.txt')

			except Exception as e:
				log(a_result + '\nError occured: ' +  str(e), log_folder, '_Log.txt')
				print( ' ->Error occured: ' + str(e))

			s_result = '\n<SCRIPT SRC> parsed started for: ' + parsefile + '\n'
			print(  ' -><SCRIPT SRC> parsed started for: ' + parsefile)
			s_result += '===================================================================\n'
			print( ' ->===================================================================')
			try:
				for stag in soup.find_all('script'):
					s_href = stag['src']
					s_href_ext = exts(s_href)

					if s_href_ext in self.css_list:
						new_s_href = joinpath(css_folder, basename(s_href))
						s_result += 'OLD href: ' + s_href + ' NEW href: ' + new_s_href + '\n'
						print( ' ->OLD href: ' +s_href + ' NEW href: ' + new_s_href)

					elif s_href_ext in self.java_list:
						new_s_href = joinpath(js_folder, basename(s_href))
						s_result += 'OLD href: ' + s_href + ' NEW href: ' + new_s_href + '\n'
						print( ' ->OLD href: ' + s_href + ' NEW href: ' + new_s_href)
					else:
						new_s_href = joinpath(others_folder, basename(s_href))
						s_result += 'OLD href: ' + s_href + ' NEW href: ' + new_s_href + '\n'
						print( ' ->OLD href: ' + s_href + ' NEW href: ' + new_s_href)

					log_s = laravel_url + new_urlpath(new_s_href)
					stag['href'] = log_s

					counts += 1
					s_result += 'OLD href: ' + s_href + ' NEW href: ' + log_s + '\n'
					print(' ->OLD href: ' + s_href + ' NEW href: ' + log_s)

				s_result += str(counts) + ' <a href> was found and processed END\n\n'
				print( ' ->'+str(counts) +  ' <a href> was found and processed END')

				if counts > 0:
					log(s_result, log_folder, '_Log.txt')

			except Exception as e:
				log(a_result + '\nError occured: ' + str(e), log_folder, '_Log.txt')
				print( ' ->Error occured: ' + str(e))

			link_result = '\n<LINK HREF> parsed started for: ' + parsefile + '\n'
			print(' -><LINK HREF> parsed started for: ' + parsefile)
			link_result += '===================================================================\n'
			print(' ->===============================================================')

			try:
				for linktag in soup.find_all('link'):
					link_href = linktag['href']
					link_href_ext = exts(link_href)

					if link_href_ext in self.css_list:
						new_href = joinpath(
							css_folder, basename(link_href))
						link_result += 'OLD href: ' + link_href + ' NEW href: ' + new_href + '\n'
						print( ' ->OLD href: ' +  link_href + ' NEW href: ' + new_href)

					elif link_href_ext in self.media_list:
						new_href = joinpath(img_folder, basename(link_href))
						copyfiles(link_href, self.build_folder+'/' +  self.laravel_image + '/' + basename(link_href))
						link_result += 'OLD href: ' + link_href + ' NEW href: ' + new_href + '\n'
						print( ' ->OLD href: ' + link_href + ' NEW href: ' + new_href)

					elif link_href_ext in self.java_list:
						new_href = joinpath(
							js_folder, basename(link_href))
						countjs += 1
						link_result += 'OLD href: ' + link_href + ' NEW href: ' + new_href + '\n'
						print( ' ->OLD href: ' + link_href + ' NEW href: ' + new_href)

					elif link_href_ext in self.font_list:
						new_href = joinpath(
							font_folder, basename(link_href))
						copyfiles(link_href, self.build_folder+'/' + self.laravel_image + '/' + basename(link_href))
						link_result += 'OLD href: ' + link_href + ' NEW href: ' + new_href + '\n'
						print( ' ->OLD href: ' + link_href + ' NEW href: ' + new_href)

					else:
						new_href = joinpath(
							others_folder, basename(link_href))
						link_result += 'OLD href: ' + link_href + ' NEW href: ' + new_href + '\n'
						print( ' ->OLD href: ' + link_href + ' NEW href: ' + new_href)

					linktag['href'] = laravel_url + new_href
					countlink += 1
				link_result += str(countlink) + \
					' <link href> was found and processed END\n\n'
				print( ' ->'+str(countlink) + ' <link href> was found and processed END')

				if countlink > 0:
					log(link_result, log_folder, '_Log.txt')
			except Exception as e:
				log(link_result + '\nError occured: ' +
					str(e), log_folder, '_Log.txt')
				print( ' ->Error occured: ' + str(e))

			img_result = '\n<IMG SRC> parsed started for: ' + parsefile + '\n'
			print(' ->< IMG SRC > parsed started for: ' + parsefile)
			img_result += '===================================================================\n'
			print(' ->===================================================================')

			try:
				for imgtag in soup.find_all('img'):
					img_src = imgtag['src']
					new_src = joinpath(img_folder, basename(img_src))
					copyfiles(img_src, self.build_folder+'/' + self.laravel_image + '/' + basename(img_src))
					imgtag['src'] = laravel_url + new_src
					countimg += 1
					img_result += 'OLD src: ' + img_src + ' NEW src: ' + new_src + '\n'
					print( ' ->OLD src: ' + img_src + ' NEW src: ' + new_src)
				img_result += str(countimg) + \
					' <img src> was found and processed END\n\n'
				print( ' ->'+str(countimg) + ' <img src> was found and processed END')
				if countimg > 0:
					log(img_result, log_folder, '_Log.txt')
			except Exception as e:
				log(img_result + '\nError occured: ' +
					str(e), log_folder, '_Log.txt')
				print( ' ->'+img_result + '\nError occured: ' + str(e))

			parsed_content = soup.prettify().replace('&gt;', '>').replace('&lt;', '<')

			final_copyto_dir = joinpath(path_dir, write_parsed_file_to)
			try:
				#print('FOLDER: ' + path_dir)
				#print('FILENAME: '+ write_parsed_file_to)
				result += 'Parsed: ' + parsefile + ' => ' + final_copyto_dir + '\n'
				print( ' ->Parsed: ' + parsefile + ' => ' + final_copyto_dir)
				localwrite_file(final_copyto_dir, parsed_content)

			except Exception as e:
				result += 'Writting error parsed: ' + parsefile + ' ' + str(e)
				print( ' ->Writting error parsed: ' + parsefile + ' ' + str(e))

			log(result, log_folder, '_log.txt')
		except Exception as e:
			log('Error occured, Unable to read this file: ' + parsefile + ' ' + str(e), log_folder, '_log.txt')
		print( '<--> Finished*** ' + final_copyto_dir)

	def file_parser(self, parsedata):
		parsefile = parsedata['filename']

		if os.path.isfile(parsefile):
			parsefile_ext = exts(parsefile)

			if parsefile_ext in self.extension_list:
				if parsefile_ext == '.js' or parsefile_ext == '.css' or parsefile_ext == '.scss':
					#copy the files to their destinated folders
					self.copyDependancy(parsedata)

				#start parsing the files to arrange the links and replace all global veriables set
				self.parser(parsedata)

			else:
				self.copyDependancy(parsedata)
				print('WARNING', ' ->Files not supported ' + basename(parsefile))


def run():
	t = threading.Thread(name='Build Laravel Started', target= BuildLaravelBackEnd())
	t.start()


if __name__ == "__main__":
	run()
