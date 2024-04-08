# Obtain command line arguments passed to the script
args <- commandArgs(trailingOnly = TRUE)

# Read the phenotype data from a specified path, specifying column names and ensuring strings are not converted to factors
phenotypeData <- read.table("/srv/scratch/cking/ralmeida/PhD/Phenotypes/bean_phenotypes.txt", sep="\t", stringsAsFactors=FALSE, header=TRUE, col.names = c("ID", "Phenotype"))

# Convert the ID column to character type to ensure consistent matching later
phenotypeData$ID <- as.character(phenotypeData$ID)

# Read the k-mer table from the first command line argument, specifying that the header is present and strings should not be converted to factors
kmerTable <- read.table(args[1], sep="\t", header=TRUE, stringsAsFactors=FALSE)

# Extract the IsolateID from the samp_id column by removing the path and retaining only the file name (without the .fasta extension)
kmerTable$IsolateID <- gsub("^.*/([^/]+)\\.fasta$", "\\1", kmerTable$samp_id)

# Filter the k-mer table to include only rows where the IsolateID matches an ID in the phenotype data
filteredKmerTable <- kmerTable[kmerTable$IsolateID %in% phenotypeData$ID, ]

# Add the corresponding phenotype to the filtered k-mer table by matching the IsolateID with the ID in the phenotype data
filteredKmerTable$Phenotype <- phenotypeData$Phenotype[match(filteredKmerTable$IsolateID, phenotypeData$ID)]

# Define the columns to retain in the final table: IsolateID, Phenotype, and any columns that include "pat" in their name
desiredColumns <- c("Isolate", "Phenotype", grep("pat", names(filteredKmerTable), value = TRUE))

# Subset the filtered k-mer table to include only the desired columns
finalTable <- filteredKmerTable[, desiredColumns]

# Write the final table to a CSV file, excluding row names and avoiding quoting the field values
write.csv(finalTable, "feature_labels_table.csv", row.names = FALSE, quote = FALSE)

# Save the final table as an RDS file for easy loading in R sessions
saveRDS(finalTable, "feature_labels_table.rds")
