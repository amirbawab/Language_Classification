import argparse
import random
import csv
import os

class CLI:
    def read(self):
        """Initialize a command line interface"""

        # Define arguments
        parser = argparse.ArgumentParser(description='Merge two csv files into one')
        parser.add_argument('-t','--text', nargs=1, help='CSV text file')
        parser.add_argument('-l','--lang', nargs=1, help='CSV language file')
        parser.add_argument('-o','--out', nargs=1, help='CSV output file')
        parser.add_argument('-O','--Out', nargs=1, help='CSV output files destination')
        parser.add_argument('-a','--algo', nargs='+', help='Algorithm id to be performed on the text')
        args = parser.parse_args()

        # Check for missing arguments
        if args.text is None or args.lang is None or (args.out is None and args.Out is None):
            print("Missing arguments")
            exit(1)

        # Prepare csv variables
        entries = {}

        # Load text csv
        if args.text is not None:
            print(">> Loading CSV text:", args.text[0])
            with open(args.text[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:

                    # Load attributes
                    id = row['Id']
                    text = row['Text']
                    
                    # Add objects
                    entries[id] = {"id":id, "text": text}

        # Load lang csv
        if args.lang is not None:
            print(">> Loading CSV language:", args.lang[0])
            with open(args.lang[0], newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    id = row['Id']
                    category = row['Category']
                    entries[id]['category'] = category

        # Apply algorithms
        if args.algo is not None:
            for algo in args.algo:
                print(">> Applying algorithm:",algo)
                if algo == "space":
                    for entry in entries:
                        entries[entry]['text'] = "".join(entries[entry]['text'].split())
                        entries[entry]['text'] = entries[entry]['text'].replace(""," ")
                elif algo == "no_space":
                    for entry in entries:
                        entries[entry]['text'] = "".join(entries[entry]['text'].split())
                elif algo == "lower":
                    for entry in entries:
                        entries[entry]['text'] = entries[entry]['text'].lower()
                elif algo == "shuffle":
                    for entry in entries:
                        splitTxt = entries[entry]['text'].split()
                        random.shuffle(splitTxt)
                        entries[entry]['text'] = " ".join(splitTxt)
                elif algo.startswith("cut"):
                    strlen = int(algo[3:])
                    for entry in entries:
                        entries[entry]['text'] = entries[entry]['text'][0:strlen]
                elif algo == "sort_lex":
                    for entry in entries:
                        entries[entry]['text'] = "".join(sorted(entries[entry]['text'], key=str.lower))
                else:
                    print(">> Algorithm:",algo,"not found!")
        # Prepare output
        if args.out is not None:
            print(">> Generating CSV:", args.out[0])
            outputFile = open(args.out[0], 'w')
            outputFile.write("Id,Category,Text\n")
            for entry in entries:
                outputFile.write("{},{},{}\n".format(entries[entry]['id'], entries[entry]['category'], 
                    entries[entry]['text']));
            outputFile.close()
        elif args.Out is not None:
            print(">> Generating CSV files in directory:", args.Out[0])
            for entry in entries:
                filename = "{}/{}/{}".format(args.Out[0], entries[entry]['category'], entries[entry]['id'])
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                outputFile  = open(filename,'w')
                outputFile.write(entries[entry]['text'])
                outputFile.close()
            
# Stat application
cli = CLI()
cli.read()
