#!/usr/bin/bash

cd "$(dirname "$0")"

if ! [ $1 ]; then
	echo "Usage: ./auto_mapping.sh <semester>"
	echo "NOTE: Assumes \'scraper.py\', \'htmlparser.py\', and \'schedulepacker.py\' have already been run"
	echo
	echo "Examples: ./auto_mapping.sh Fall2022, "
	echo "          ./auto_mapping.sh Summer2023, etc."
	echo
	echo "Plots will be stored in './saved_plots/{semester}/heatmaps/' and './saved_plots/{semester}/bookings/'"
	echo
	exit
fi

heatmap_dir="./saved_plots/$1/heatmaps"
bookings_dir="./saved_plots/$1/bookings"

echo "Saving to $heatmap_dir/ and $bookings_dir/"

mkdir -p "${heatmap_dir}/CSCE"
mkdir -p "${heatmap_dir}/EENG"
mkdir -p "${bookings_dir}"

python3 heatmap.py -sd ${heatmap_dir}/AllDept.png
echo Saved AllDept.png
python3 heatmap.py -sd ${heatmap_dir}/CSCE/CSCEDept.png CSCE 
echo Saved CSCEDept.png
python3 heatmap.py -sd ${heatmap_dir}/CSCE/CSCE1-2.png CSCE1 CSCE2
echo Saved CSCE1-2.png
python3 heatmap.py -sd ${heatmap_dir}/CSCE/CSCE3-4.png CSCE3 CSCE4
echo Saved CSCE3-4.png
python3 heatmap.py -sd ${heatmap_dir}/CSCE/CSCE5-6.png CSCE5 CSCE6
echo Saved CSCE5-6.png
python3 heatmap.py -sd ${heatmap_dir}/CSCE/CSCE3-6.png CSCE3 CSCE4 CSCE5 CSCE6
echo Saved CSCE3-6.png
python3 heatmap.py -sd ${heatmap_dir}/EENG/EENGDept.png EENG 
echo Saved EENGDept.png
python3 heatmap.py -sd ${heatmap_dir}/EENG/EENG1-2.png EENG1 EENG2
echo Saved EENG1-2.png
python3 heatmap.py -sd ${heatmap_dir}/EENG/EENG3-4.png EENG3 EENG4
echo Saved EENG3-4.png
python3 heatmap.py -sd ${heatmap_dir}/EENG/EENG5-6.png EENG5 EENG6
echo Saved EENG5-6.png
python3 heatmap.py -sd ${heatmap_dir}/EENG/EENG3-6.png EENG3 EENG4 EENG5 EENG6
echo Saved EENG3-6.png
python3 heatmap.py -sd ${heatmap_dir}/CSCE_EENG.png CSCE EENG
echo Saved CSCE_EENG.png
python3 heatmap.py -sd ${heatmap_dir}/CircuitAnalysis.png EENG2610 EENG2611
echo Saved CircuitAnalysis.png
python3 heatmap.py -sd ${heatmap_dir}/DigitalLogic.png EENG2710 EENG2711
echo Saved DigitalLogic.png
python3 heatmap.py -sd ${heatmap_dir}/SigAndSystems.png EENG2620 EENG2621
echo Saved SigAndSystems.png

python3 roombookingview.py -sd ${bookings_dir}/B242.png B242
echo Saved B242.png
python3 roombookingview.py -sd ${bookings_dir}/B288.png B288
echo Saved B288.png
python3 roombookingview.py -sd ${bookings_dir}/B207.png B207
echo Saved B207.png
python3 roombookingview.py -sd ${bookings_dir}/B227.png B227
echo Saved B227.png
python3 roombookingview.py -sd ${bookings_dir}/D215.png D215
echo Saved D215.png
python3 roombookingview.py -sd ${bookings_dir}/K120.png K120
echo Saved K120.png
python3 roombookingview.py -sd ${bookings_dir}/K150.png K150
echo Saved K150.png

