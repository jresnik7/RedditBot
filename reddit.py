import praw
import creds as r
import requests
import os


class REDDIT():
    """
    """
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=r.client_id,
            client_secret=r.client_secret,
            username=r.username,
            password=r.password,
            user_agent=r.user_agent
        )
        self.visited_posts = []

    def __load_visited__(self):
        v = []
        with open('visited.txt') as f:
            v = f.readlines()
        for line in v:
            self.visited_posts.append(line.strip())

    def __add_visited__(self, post_url):
        self.visited_posts.append(post_url)
        v = open('visited.txt', 'a')
        v.write(post_url + '\n')
        v.close()

    def start_loop(self):
        while True:
            command = input(">")
            self.__process_command__(command)

    def __process_command__(self, cmd):
        command = cmd.split(' ')
        func = command.pop(0)
        getattr(self, func)(*command)

    def __get_image_urls__(self, sub, number=1):
        ret_array = []
        for submission in self.reddit.subreddit(sub).hot(limit=number):
            ret_array.append(submission.url)
        return ret_array

    def dlimg(self, sub, number=1):
        urls = self.__get_image_urls__(sub, int(number))
        extension = '0'
        image_files = []
        for url in urls:
            if url in self.visited_posts:
                pass
            else:
                # Filter image file types
                if '.png' in url:
                    extension = '.png'
                elif '.jpg' in url or '.jpeg' in url:
                    extension = '.jpeg'
                elif 'imgur' in url:
                    url += 'jpeg'
                    extension = '.jpeg'
                else:
                    print("No image found on this url")

                if extension != '0':
                    image = requests.get(url, allow_redirects=False)
                    file_name = url[url.rfind('/') + 1:] + extension

                    if image.status_code == 200:
                        with open('images/' + file_name, mode='wb') as meme_file:
                            meme_file.write(image.content)
                        self.__add_visited__(url)
                        print(f"Images found and saved as {file_name} [{len(image_files)}]")
                        image_files.append(file_name)

                extension = '0'

        self.__image_keep__(image_files)

    def __image_keep__(self, image_files):
        x = 0
        for image in image_files:
            answer = input('Keep file [' + str(x) + '] (y/ya/n/na)?')
            if answer == 'n':
                os.remove(image)
                x += 1
            elif answer == 'ya':
                return
            elif answer == 'na':
                for image in image_files:
                    os.remove('images/' + image)
                return
            elif answer == 'y':
                x += 1
            else:
                print('Invalid response (y/ya/n/na)')

    def exit(self):
        quit()


if __name__ == '__main__':
    redd = REDDIT()
    redd.start_loop()
