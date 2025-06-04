from utils import LinkProcessor

def main():
    # Initialize processor with your CSV file
    processor = LinkProcessor('links.csv')
    
    try:
        processor.process_links()
    finally:
        processor.cleanup()
        processor.save_status()


if __name__ == "__main__":
    main()
