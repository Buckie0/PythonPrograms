#!/bin/bash

if [ -z "$1" -o -z "$2" -o -z "$3" ]; then
    echo Usage: `basename $0` {infile} {snaplen} {displayfilter}
    exit 1
fi

# binaries
TSHARK=/opt/local/bin/tshark
EDITCAP=/opt/local/bin/editcap

# parameters
TMPFILE=$(mktemp pcap.XXXXXXXXXX)
INFILE=$1
OUTFILE=$1.out
SNAPLEN=$2
DFILTER=$3

cp "${INFILE}" "${TMPFILE}"

echo "Filtering packets..."
INPUT=$(${TSHARK} -R "${DFILTER}" -r "${INFILE}" -T fields -e frame.number)
__max=`echo ${INPUT} | wc -w`
__i=0

echo "Writing pcap..."
for x in ${INPUT[*]}
do
    # show progress
    ((__i++))
    printf "${__i}/${__max} ($((${__i}*100/${__max}))%%)\r"

    # truncate the specified packet, copy the resulting pcap
    # back to the temporary working file for the next iteration
    ${EDITCAP} -s "${SNAPLEN}" "${TMPFILE}" "${OUTFILE}" "${x}" > /dev/null
    cp "${OUTFILE}" "${TMPFILE}"
done

echo
rm "${TMPFILE}"
# rm "${INFILE}"
echo "Wrote ${OUTFILE}"

# To use:
# $ snap.sh SIP_CALL_RTP_G711.pcap 54 rtp.payload
# Filtering packets...
# Writing pcap...
# 1445/    1445 (100%)
# Wrote SIP_CALL_RTP_G711.pcap.out