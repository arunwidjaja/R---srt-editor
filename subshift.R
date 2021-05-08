# Subtitle Shifter
#### REQUIRED FILES ####

# Input:
# an .srt subtitle file that has ".en" in the name.

# Output:
# an .srt subtitle file, shifted according to the constants - see CONSTANTS section

#### LIBRARIES ####

library(stringr)

#### CONSTANTS ####

# milliseconds to shift file
SHIFT_AMOUNT=-12000

#### READING FILE ####

setwd("C:/Users/Arun Widjaja/Documents/R Scripts/srt editor")
fn_sub=dir(pattern="\\.en\\.srt")

print(paste("READING:",fn_sub))
sub_raw=readLines(fn_sub)

#### PARSING FILE ####

# read .srt file as a 1-column data frame
sub_parsed=data.frame(sub_raw,stringsAsFactors=F)
names(sub_parsed)="sub"

# add column containing starting timestamps of each subtitle
sub_parsed$t1=str_extract(sub_parsed$sub,"\\d{2}:\\d{2}:\\d{2},\\d{3}")

# add column containing ending timestamps of each subtitle
sub_parsed$t2=str_extract(sub_parsed$sub,"-->.*\\d{2}:\\d{2}:\\d{2},\\d{3}")
sub_parsed$t2=str_replace(sub_parsed$t2,"-->\\s{1,}","")

# replace commas with periods to fit timestamp format
sub_parsed$t1=str_replace(sub_parsed$t1,",",".")
sub_parsed$t2=str_replace(sub_parsed$t2,",",".")

# get indices of rows containing timestamps
index_times=which(!is.na(sub_parsed$t1))

# split times into h, m, s, ms
t1=str_split(sub_parsed$t1,pattern=":")
t2=str_split(sub_parsed$t2,pattern=":")

# convert to ms and apply shift
for(i in 1:nrow(sub_parsed)){
  sub_parsed$t1[i]=as.numeric(t1[[i]][1])*3600000+as.numeric(t1[[i]][2])*60000+as.numeric(t1[[i]][3])*1000
  sub_parsed$t2[i]=as.numeric(t2[[i]][1])*3600000+as.numeric(t2[[i]][2])*60000+as.numeric(t2[[i]][3])*1000
}
sub_parsed$t1=as.numeric(sub_parsed$t1)+SHIFT_AMOUNT
sub_parsed$t2=as.numeric(sub_parsed$t2)+SHIFT_AMOUNT

# convert back to h, m, s, ms and overwrite original times
sub_parsed$t1=paste(
  str_pad(trunc(sub_parsed$t1/3600000),2,"left","0"),":",
  str_pad(trunc((sub_parsed$t1 %% 3600000)/60000),2,"left","0"),":",
  str_pad(trunc((sub_parsed$t1 %% 60000)/1000),2,"left","0"),",",
  str_pad((sub_parsed$t1 %% 1000),3,"right","0"),
  sep=""
)
sub_parsed$t2=paste(
  str_pad(trunc(sub_parsed$t2/3600000),2,"left","0"),":",
  str_pad(trunc((sub_parsed$t2 %% 3600000)/60000),2,"left","0"),":",
  str_pad(trunc((sub_parsed$t2 %% 60000)/1000),2,"left","0"),",",
  str_pad((sub_parsed$t2 %% 1000),3,"right","0"),
  sep=""
)
sub_parsed$sub[index_times]=paste(sub_parsed$t1[index_times],"-->",sub_parsed$t2[index_times])

#### WRITING FILE ####

writeLines(sub_parsed$sub,paste("SHIFTED -",fn_sub))

