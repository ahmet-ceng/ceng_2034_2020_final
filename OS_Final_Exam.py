import os 
import urllib.request
import hashlib
import sys

#Ahmet Oral 180709008
#If there is any problem please contact me. My email:ahmetoral@posta.mu.edu.tr

#Our list of url's.
#You can add any number of url's if you want,program will save them with different names and find duplicated ones.
#You can add more than one copies of an image program will find all the copies and delete them until there is 1 original left.
#Any url type will work including gifs.But it has to state its type at the end.(like https...asd.gif)

url_list=[
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"
]

#*****Please update the location before using the program*****
location = '/home/ahmet/Desktop/Photos/'

#creating child process using os.fork() method
test = os.fork()

# n greater than 0  means parent process 
if (test > 0): 
	#To avoid orphan process I used os.wait()		
	os.wait()
	print("Parent process id is : ", os.getpid()) 

    
# n equals to 0 means child process 
else: 
	
	print("Child process id is : ", os.getpid()) 
	
	print("\nBeginning file download...")
	
	#variable to name images as photo1/photo2/photo97
	image_number = 0
	
	#loops throuh the url_list and downloads each url
	for i in url_list:
	
		#incrementing counter	
		image_number+=1	
		
		#Determining the type with better way! (I will put older versions to the report)
		#There are probably much more easier and accurate ways to find the image format of the url but I wanted to do it by myself without looking it from online :D
		#I take the last 5 digits of the url and slice it after the dot(.).
		#I left with the type like: jpeg/png/gif...
		image_type = i[-5:].split(".",1)[1] 
		
		#To be able to use it as format I add . to it so it becomes like: .jpeg/.gif	
		image_type = '.' + image_type

		#Name of the image(for ex.'Photo1.jpeg')
		image_name='photo'+ str(image_number) + image_type
	
		#Name and location of the image.
		name_and_location = location + image_name
		
		#Downloads the image to the given location with given name.
		urllib.request.urlretrieve(i, name_and_location)

	print("All files downloaded succesfully!\n")
	
#***From now on program will check files in the directory to find and delete duplicates.***

	#This function takes the file in provided location and returns it hash code
	def hashfinder (file):
		md5_hash = hashlib.md5()
		photo = open(file, "rb")
		md5_hash.update(photo.read())
		return(md5_hash.hexdigest())
	
	#Creating list of the all photos in directory
	list_of_photos = os.listdir("/home/ahmet/Desktop/Photos")

	#Creating hash list of photos.
	hash_list=[]
	for i in list_of_photos:
		hash_list.append(hashfinder(location + i))
	
	#Creating list of the all photos in directory
	list_of_photos = os.listdir("/home/ahmet/Desktop/Photos")
	
	#Small algorithm to find duplicates in the hash_list
	#This algorith creates new list called duplicates and places duplicated hashes inside.
	x=set(hash_list)
	duplicates=[]
	for c in x:
		if(hash_list.count(c)>1):
			duplicates.append(c)
	
	#This loop prints hash codes of images in directory
	for i in list_of_photos:
		print(i," :  ", hashfinder(location + i) )
		
	#This shows how many duplicates there are and their hash codes.
	amount_of_duplicates = len(duplicates)
	print("\nThere are duplicates of this",amount_of_duplicates,"image: " ,duplicates,"\n")
	
	#I created a while loop to ask user if they want to delete duplicated files
	while True:
		yes_no = input("Would you like to delete duplicated photos from directory? (y/n)")
		if yes_no == "y":
			
			while True:
			
				
				#This loop finds the index of duplicated hash codes in the hash_list.Than it finds the corresponding photo in directory.
			#After finding duplicated photos it deletes one of the copies.
				for i in duplicates:
					index = hash_list.index(i)
					files_to_be_deleted = list_of_photos.pop(index)
					os.remove(location + files_to_be_deleted )
				
				#Creating lists again to update adresses.
				list_of_photos = os.listdir("/home/ahmet/Desktop/Photos")

				#clearing and creating list again to update.
				hash_list.clear()
				for i in list_of_photos:
					hash_list.append(hashfinder(location + i))
				
				
				#clearing the list before running to prevent overlapping.
				duplicates.clear()
				#same algorithm to find duplicates and put them in a list.
				x=set(hash_list)
				duplicates=[]
				for c in x:
					if(hash_list.count(c)>1):
						duplicates.append(c)
				
				
				#if there are no more duplicats exit loop.
				if len(duplicates) == 0:
					break
					
				
	
			
			print("Copies of",amount_of_duplicates, "duplicated files are deleted succesfully!\n")
			break
		elif yes_no == "n":
			print("\nDuplicated files won't be deleted.")
			break
		else:
			print("\n*** Undefined input.Please only enter 'y' or 'n' ***\n")


