# ex1


## Background

1. I have no previous experiance with any of the subjects introduced here, including FastAPI.
2. I have some work experiance with Python.


## Usage

1. Edit [consts.py](consts.py) to suite your work environmwnt
2. To deploy

        python3.10 ./deploy.py

3. To run:

        fastapi dev ./main.py


## Work environment

I was using:

1. Visal code with python support.
2. Postman for posting requests.
3. Python v3.10.


## Work effort
1. 19/07/2024 - First work day. Few hours on Part1. Got the two models to work.
2. 25/07/2024 - Second day of work. full work day. Part2. Creating the FastAPI interface, deploy script and struggling with the streaming problem.
3. 26/07/2024 - Third day of work. full work day. Trying more on the streaming problem, cleanups and uploading to github.

Roughly, trying to solve the streaming issue is responsible for around 40% of the work efffort done. This is still not solved. See Streaming below.

## Known Issues

1. When using deploy.py, if a required packageis missing the script will try to install it but even if it succeeds, you'll need to re-run deploy.py for the changes to take effect. I've searched several solutions for this, one of them is coded in utils.install_and_import() but non really worked.

2. Streaming. See below.


## Streaming

A large percentage of my work effort was on the streaming problem.
I've tried many directions from public samples and my own guesses. still, this remains unsolved. 
So, currently, the request is waiting untill all the reply is generated before getting and displaying it.

### Some of the stuff I tried was
1. Using a regular browser instead of Postman thinking it might not support event streaming.
2. Using FastAPI underlaying web directly and passing command line argumets to it to disable any caching of results. For example, I was trying to use: uvicorn main:app --host 0.0.0.0 --port 8000 --h11-max-incomplete-event-size 5.
4. Using verious combinations of async / non async functions for the main end-point and the Generator used. I need to read more on this topic.
5. Using several llama.cpp API's like create_completion() and create_chat_completion().
6. Trying by-the-book tutorial samples from the internet. None worked.

### Some of the references I visited for this problem
- https://github.com/run-llama/llama_index/issues/10517
- https://github.com/abetlen/llama-cpp-python/discussions/319
- https://stackademic.com/blog/streaming-llm-responses-using-fastapi-deb575554397
- https://dev.to/ashraful/fastapi-streaming-response-39c5

### FastAPI doc sample that is also NOT working as-is
https://github.com/tiangolo/fastapi/discussions/10701


## Example usgae

See [examples.md](examples.md)
