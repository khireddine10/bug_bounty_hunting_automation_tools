import argparse
import concurrent.futures
import requests
import requests_cache

# Set up the argument parser
parser = argparse.ArgumentParser()
parser.add_argument("url", help="the URL of the domain to send the requests to")
parser.add_argument("file", help="a file containing a list of words to concatenate to the URL")
parser.add_argument("output_file", help="the name of the file to output the URLs to")
parser.add_argument("thread", help="number of threads to use in requests")
args = parser.parse_args()

# Get the URL and file from the command line arguments
url = args.url
filename = args.file
output_file = args.output_file
threads_num = args.thread 
# Open the file and read the list of words
with open(filename, 'r') as file:
  words = file.readlines()

# Set up the connection pool and cache
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('http://', adapter)
session.mount('https://', adapter)
requests_cache.install_cache('options_request_cache', backend='sqlite', expire_after=3600)

# Function to send an OPTIONS request to a file URL
def send_request(file_url):
  response = session.options(file_url)
  return file_url, response.status_code

# Create a thread pool with 4 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=int(threads_num)) as executor:
  # Submit the requests to the thread pool
  futures = [executor.submit(send_request, f"{url}/{word.strip()}") for word in words]

  # Open the output file
  with open(output_file, 'w') as outfile:
    # Iterate through the completed requests
    for future in concurrent.futures.as_completed(futures):
      file_url, status_code = future.result()
      if status_code == 200:
        # Write the URL to the output file
        outfile.write(f"{file_url}\n")

print(f"URLs that responded with 200 OK were written to {output_file}")
