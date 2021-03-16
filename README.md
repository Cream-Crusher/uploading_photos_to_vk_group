# Uploading photos to vk group

Script for uploading comics to the VKontakte group.
 
# How to start

Create a file .env.

Create a ['Standalone'](https://vk.com/editapp?act=create) application.

Python3 should be already installed.

Use pip to install dependencies:

```bash
pip install -r requirements.txt
```

### Environment variables

- ACCESS_TOKEN
- CLIENT_ID
- GROUP_ID

example .env:

```
CLIENT_ID=1111111
ACCESS_TOKEN=5607b93462c0a7e6b07d4e1892493e92d13c94e2391f80131edf0853c1e05b29e968rb2w265589cftu9
```

### Run

```
$ python working_with_the_vk_api.py.py
```

# You will see

Comics in the group.

# If there are no required group permissions or there is a problem with getting ACCESS_TOKEN

Use the file getting_access_to_group.py

```
$ python getting_access_to_group.py
```

In the console, you will see the URL link. Copy and paste it into your browser and click allow access.

To get access_token, click on the link and copy your access_token.

[If you still have any questions](https://devman.org/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/).


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org).
