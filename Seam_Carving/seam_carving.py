import sys
import time
from resizeable_image import ResizeableImage

def usage():
    sys.stderr.write("Usage: {} image_file\n".format(sys.argv[0]))
    exit(1)

def benchmark_seam(filename):
    """Benchmark naive and DP seam carving algorithms."""
    #load the image
    print("Loading image: {}".format(filename))
    image = ResizeableImage(filename)
    
    #display image dimensions
    print("Image dimensions: {}x{} (width x height)".format(image.width, image.height))
    print("Total pixels: {}".format(image.width * image.height))
    print()
    
    #benchmark DP algorithm
    print("Running dynamic programming algorithm...")
    start_time = time.time()
    seam_dp = image.best_seam(dp=True)
    dp_time = time.time() - start_time
    print("DP algorithm completed in {:.6f} seconds".format(dp_time))
    
    
    #benchmark naive algorithm (only for small images)
    if image.width * image.height < 1000:
        print("Running naive recursive algorithm...")
        start_time = time.time()
        seam_naive = image.best_seam(dp=False)
        naive_time = time.time() - start_time
        print("Naive algorithm completed in {:.6f} seconds".format(naive_time))
        
        #compare results
        print("Performance comparison:")
        print("Speedup: {:.2f}x faster with DP".format(naive_time / dp_time))
    else:
        print("Image too large for naive algorithm (would take too long)")
        print("Naive algorithm has exponential complexity: O(3^height)")
        print("For this image, that would be approximately 3^{} operations".format(image.height))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    
    filename = sys.argv[1]
    benchmark_seam(filename)