args <- commandArgs(trailingOnly = TRUE)

phenotypeData <- read.table("/srv/scratch/cking/ralmeida/PhD/Phenotypes/bean_phenotypes.txt", sep="\t", stringsAsFactors=FALSE, header=TRUE, col.names = c("ID", "Phenotype"))
phenotypeData$ID <- as.character(phenotypeData$ID) # Ensure ID column is treated as character

kmerTable <- read.table(args[1], sep="\t", header=TRUE, stringsAsFactors=FALSE)

kmerTable$IsolateID <- gsub("^.*/([^/]+)\\.fasta$", "\\1", kmerTable$samp_id)

filteredKmerTable <- kmerTable[kmerTable$IsolateID %in% phenotypeData$ID, ]

filteredKmerTable$Phenotype <- phenotypeData$Phenotype[match(filteredKmerTable$IsolateID, phenotypeData$ID)]

desiredColumns <- c("IsolateID", "Phenotype", grep("pat", names(filteredKmerTable), value = TRUE))

finalTable <- filteredKmerTable[, desiredColumns]

write.csv(finalTable, "feature_labels_table.csv", row.names = FALSE, quote = FALSE)
saveRDS(finalTable, "feature_labels_table.rds")
