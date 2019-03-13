#!/bin/ksh
#
# Setupfile including paths

run=$1
date=$2
mem=$3
lagg=$4
assimc=$5

export EXP=AROM

################calculate time windows and time shifts ###################
typeset -Z2 assimc1 assimc2 assimc3 assimc4 assimc5 assimc6 assimc7 assimc8 assimc9
assimc1=$(($assimc))
assimc2=$(($assimc * 2))
assimc3=$(($assimc * 3))
assimc4=$(($assimc * 4))
assimc5=$(($assimc * 5))
assimc6=$(($assimc * 6))
assimc7=$(($assimc * 7))
assimc8=$(($assimc * 8))
assimc9=$(($assimc * 9))

export p1date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc1}:00 | cut -c 1-8)
export p1run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc1}:00 | cut -c 9-10)
export p2date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc2}:00 | cut -c 1-8)
export p2run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc2}:00 | cut -c 9-10)
export p3date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc3}:00 | cut -c 1-8)
export p3run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc3}:00 | cut -c 9-10)
export p4date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc4}:00 | cut -c 1-8)
export p4run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc4}:00 | cut -c 9-10)
export p5date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc5}:00 | cut -c 1-8)
export p5run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc5}:00 | cut -c 9-10)
export p6date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc6}:00 | cut -c 1-8)
export p6run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc6}:00 | cut -c 9-10)
export p7date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc7}:00 | cut -c 1-8)
export p7run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc7}:00 | cut -c 9-10)
export p8date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc8}:00 | cut -c 1-8)
export p8run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc8}:00 | cut -c 9-10)
export p9date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc9}:00 | cut -c 1-8)
export p9run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${assimc9}:00 | cut -c 9-10)
export n1run=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${lagg}:00 | cut -c 9-10)
export n1date=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${lagg}:00 | cut -c 1-8)
export n1mm=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${lagg}:00 | cut -c 5-6)
export n1dd=$(/home/ms/at/kmcw/bin/datecalc ${date}${run} -f -t -${lagg}:00 | cut -c 7-8)

export hh1=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t -1:00 | cut -c 9-10)
export date1=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t -1:00 | cut -c 1-8)
export hh2=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t +1:00 | cut -c 9-10)
export date2=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t +1:00 | cut -c 1-8)
export hh3=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t -2:00 | cut -c 9-10)
export date3=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t -2:00 | cut -c 1-8)
export hh4=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t +2:00 | cut -c 9-10)
export date4=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t +2:00 | cut -c 1-8)
export hh5=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t -3:00 | cut -c 9-10)
export date5=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t -3:00 | cut -c 1-8)
export hh6=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t +3:00 | cut -c 9-10)
export date6=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t +3:00 | cut -c 1-8)
export ficleft=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t -1:30 | cut -c 1-12)
export ficright=$(/home/ms/at/kmcw/bin/datecalc $date$run -f -t +1:30 | cut -c 1-12)
###########################################################################

##################Directories#####################
export MY_DIR=/home/ms/at/kmcw/ECF
export DATADIR=${MY_DIR}/DATA/${date}/${run}/MEM_${mem}
export LBCDIR=${DATADIR}/LBC
export LBCIFS=/sc1/tcwork/zat/lb/ecdiss
export LBCHIS=/zat2/COUPLING/ARCHIVE_4_LAEFCOUPL
export COUPLDIR=${DATADIR}/COUPL
export C927DIR=${DATADIR}/927
export C927SURFDIR=${DATADIR}/927SURF
export C001DIR=${DATADIR}/001
export SSTEXDIR=${DATADIR}/SSTEX
export ADDSURFDIR=${DATADIR}/ADDSURF
export BATORDIR=${MY_DIR}/DATA/${date}/${run}/BATOR
export BATOR3DIR=${MY_DIR}/DATA/${date}/${run}/BATOR3D
export OBSDIR=${MY_DIR}/DATA/${date}/${run}/OBSERVATIONS/OBS
export OBSDIRLAEF=/sc1/tcwork/zat/lb/LAEF_11km/obs
export OBSDIR3D=${MY_DIR}/DATA/${date}/${run}/OBSERVATIONS/OBS3D
export MINIMDIR=${DATADIR}/MINIMIZATION
export CANARIDIR=${DATADIR}/CANARI
export SCREENDIR=${DATADIR}/SCREENING
export PROGRIDDIR=${DATADIR}/PROGRID
export CLIMDIR=${MY_DIR}/CLIM
export BINDIR=${MY_DIR}/BIN
export NAMELDIR=${MY_DIR}/NAMEL
export LOGDIR=${DATADIR}/LOG
export BMATRIXDIR=/perm/ms/at/kmek/3Dvar/BMATRIX
export VMATRIXDIR=/perm/ms/at/kmek/VMATRIX
export MF_OBSDIR=/panfs/panfs.zamg.at/scratch/vhmod/prod/AROME/BACKUP_OPLACE/DATA/${date}_${run}
###################################################

######depending directories #############################
export GUESSDIR1=${MY_DIR}/DATA/${p1date}/${p1run}/MEM_${mem}/001
export GUESSDIR2=${MY_DIR}/DATA/${p2date}/${p2run}/MEM_${mem}/001
export GUESSDIR3=${MY_DIR}/DATA/${p3date}/${p3run}/MEM_${mem}/001
export GUESSDIR4=${MY_DIR}/DATA/${p4date}/${p4run}/MEM_${mem}/001
export GUESSDIR5=${MY_DIR}/DATA/${p5date}/${p5run}/MEM_${mem}/001
export GUESSDIR6=${MY_DIR}/DATA/${p6date}/${p6run}/MEM_${mem}/001
export GUESSDIR7=${MY_DIR}/DATA/${p7date}/${p7run}/MEM_${mem}/001
export GUESSDIR8=${MY_DIR}/DATA/${p8date}/${p8run}/MEM_${mem}/001
export GUESSDIR9=${MY_DIR}/DATA/${p9date}/${p9run}/MEM_${mem}/001
##########################################################

##################Input and output files#####################
export OBSFILE1=${OBSDIR}/obsoul_taw_${date}_${run}0000.asc
export OBSFILE2=${OBSDIR}/obsoul_${date}_${run}0000.asc
export OBSFILE3=${OBSDIR}/obs_short_${date}${run}.tar
export OBSFILE3h1=${OBSDIR}/obs_short_${date1}${hh1}.tar
export OBSFILE3h2=${OBSDIR}/obs_short_${date2}${hh2}.tar
export OBSFILE3h3=${OBSDIR}/obs_short_${date3}${hh3}.tar
export OBSFILE3b=${OBSDIR}/obs_foreign_${date}${run}.tar
export OBSFILE3bh1=${OBSDIR}/obs_foreign_${date1}${hh1}.tar
export OBSFILE3bh2=${OBSDIR}/obs_foreign_${date2}${hh2}.tar
export OBSFILE3bh3=${OBSDIR}/obs_foreign_${date3}${hh3}.tar
export OBSFILE4=${OBSDIR}/obsoul_temp_${date}_${run}0000.asc
export OBSFILE4a=${OBSDIR}/obsoul_pseudosounding_${date}_${run}0000.asc
export OBSFILE5=${OBSDIR}/obsoul_pilot_${date}_${run}0000.asc
export OBSFILE6=${OBSDIR}/obsoul_ship_${date}_${run}0000.asc
export OBSFILE7=${OBSDIR}/obsoul_profiler_${date}_${run}0000.asc
export OBSFILE13=${OBSDIR}/obsoul_metar_${date}_${run}0000.asc
export OBSFILE14=${OBSDIR}/obsoul_hydro_${date}_${run}0000.asc
export OBSFILE14a=${OBSDIR}/obsoul_schiwm_${date}_${run}0000.asc
export OBSFILE18=$OBSDIR3D/"SAFNWC_MSG3_HRW__"${date}${run}"00_EUROPE_______BEUM.buf"
export GPSOBSFILE=$OBSDIR3D/OBSOUL.TU.${date}${run}00.plusproch
export GUESSFILE1=${GUESSDIR1}/ICMSH${EXP}+00${assimc1}
export GUESSFILE2=${GUESSDIR2}/ICMSH${EXP}+00${assimc2}
export GUESSFILE3=${GUESSDIR3}/ICMSH${EXP}+00${assimc3}
export GUESSFILE4=${GUESSDIR4}/ICMSH${EXP}+00${assimc4}
export GUESSFILE5=${GUESSDIR5}/ICMSH${EXP}+00${assimc5}
export GUESSFILE6=${GUESSDIR6}/ICMSH${EXP}+00${assimc6}
export GUESSFILE7=${GUESSDIR7}/ICMSH${EXP}+00${assimc7}
export GUESSFILE8=${GUESSDIR8}/ICMSH${EXP}+00${assimc8}
export GUESSFILE9=${GUESSDIR9}/ICMSH${EXP}+00${assimc9}
export SOILGUESSFILE1=${GUESSDIR1}/ICMSH${EXP}+00${assimc1}.sfx
export SOILGUESSFILE2=${GUESSDIR2}/ICMSH${EXP}+00${assimc2}.sfx
export SOILGUESSFILE3=${GUESSDIR3}/ICMSH${EXP}+00${assimc3}.sfx
export SOILGUESSFILE4=${GUESSDIR4}/ICMSH${EXP}+00${assimc4}.sfx
export SOILGUESSFILE5=${GUESSDIR5}/ICMSH${EXP}+00${assimc5}.sfx
export SOILGUESSFILE6=${GUESSDIR6}/ICMSH${EXP}+00${assimc6}.sfx
export SOILGUESSFILE7=${GUESSDIR7}/ICMSH${EXP}+00${assimc7}.sfx
export SOILGUESSFILE8=${GUESSDIR8}/ICMSH${EXP}+00${assimc8}.sfx
export SOILGUESSFILE9=${GUESSDIR9}/ICMSH${EXP}+00${assimc9}.sfx
export PGDFILE_FA=${C927SURFDIR}/PGD_${EXP}.fa
export BATORODBFILE=${BATORDIR}/ecma_raw.tar
export BATOR3DODBFILE=${BATOR3DIR}/ECMA_merged.tar
export SSTEXANAFILE=${C927DIR}/ELSCF${EXP}ALBC000
export SSTEXRESULTFILE=${SSTEXDIR}/AROME_SSTOK
export ADDSURFRESULTFILE=${ADDSURFDIR}/ICMSH${EXP}+${assimc1}_addsurf
export CANARIANAFILE=${CANARIDIR}/ICMSHCYCL+0000
export CANARIANAFILESURF=${CANARIDIR}/ICMSHCYCL+0000.sfx
export SCREENRESULTFILE=${SCREENDIR}/ECMA_screen.tar
export SCREENSURFRESULTFILE=${SCREENDIR}/ECMA_surf.tar
export MINIMRESULTFILE=${MINIMDIR}/MXMINI999+0000_blend
###########################################################

###################Namelists#######################
export NAMEL901=${NAMELDIR}/c901_nam36t1
export NAMELGL=${NAMELDIR}/gl_namel_ecmwf
export NAMELADDSURFold=${NAMELDIR}/namelist_addsurf_cy36t1
export NAMELADDSURF=${NAMELDIR}/namelist_addsurf_cy40t1
export NAMEL927=${NAMELDIR}/namel_927_CY40T1_2.5km_90L
export NAMEL927_GLO=${NAMELDIR}/namel_927_CY40T1_2.5km_90L_glob
export NAMEL927ADDS=${NAMELDIR}/namel_927_CY40T1_2.5km_90L_addsurf
export NAMEL927ADDS_GLO=${NAMELDIR}/namel_927_CY40T1_2.5km_90L_addsurf_glob
export NAMEL927SURFEX=${NAMELDIR}/927surfex_CY40T1.nam
export NAMEL927SURF=${NAMELDIR}/927surf_CY40T1_2.5km.nam
export NAMEL927SURF_GLO=${NAMELDIR}/927surf_CY40T1_2.5km.nam_glob
export NAMEL001SURFEX=${NAMELDIR}/namelist_surfex_arome_cy40t1_sha
export NAMEL001=${NAMELDIR}/namel_001_CY40T1_sppt_fpos_saphir_
export NAMELLAMFLAG=${NAMELDIR}/namelist_lamflag_cy40t1
export NAMELBATOR=${NAMELDIR}/namelist_bator_cy40t1
export BLACKLIST1=${CLIMDIR}/LISTE_NOIRE_DIAP
export BLACKLIST2=${CLIMDIR}/LISTE_NOIRE_DIAP3D
export BLACKLIST3=${CLIMDIR}/LISTE_LOC3D
export NAMELBATOR3D=${NAMELDIR}/namelist_bator3D_cy40t1
export NAMELIASICHAN=${NAMELDIR}/iasichannels
export NAMELRGB=${NAMELDIR}/namelist_rgb
export NAMELLAMFLAG3D=${NAMELDIR}/namelist_lamflag3D_cy40t1
export NAMELCRISCHAN=${NAMELDIR}/namelist_cris331
export LIST_GPS=${CLIMDIR}/LIST_GPSSOL
export NAMELOIMAIN=${NAMELDIR}/namelist_oimain_cy40t1
export NAMELCANARI=${NAMELDIR}/namelist_canari_cy40t1
export NAMELMINIM=${NAMELDIR}/namelist_minim_cy40t1
export NAMELBLEND=${NAMELDIR}/namelist_blend_cy40t1
export NAMELSCREEN=${NAMELDIR}/namelist_screening_cy40t1
export NAMELSSTEX1=${NAMELDIR}/namelist_sstexchange1_cy40t1
export NAMELSSTEX2=${NAMELDIR}/namelist_sstexchange2_cy40t1
######################################################

#####################Binaries#########################
export BINGL=${BINDIR}/gl_grib_api_def
export BINADDSURF=${BINDIR}/ADDSURF_cy40t1
export BIN901=${BINDIR}/MASTER_901_cy36t1
export BINMASTER=${BINDIR}/cy40t1_MASTERODB_WASTL
export BATORBIN=${BINDIR}/BATOR_cy40t1
export MERGEOBSBIN=${BINDIR}/obsoul_merge_new.pl
export SHUFFLEBIN=${BINDIR}/odbtools_cy40t1.x
export MERGEBIN=${BINDIR}/merge_ioassign
export IOASSIGNBIN=${BINDIR}/ioassign_cy40t1
export CIOASSIGNBIN=${BINDIR}/create_ioassign_cy40t1
export BINSNOWGRID3=${BINDIR}/cy40t1_SNOWGRID3
export BINSNOWGRID4=${BINDIR}/cy40t1_SNOWGRID4
export BLENDBIN=${BINDIR}/BLEND_cy40t1
export BLENDSURBIN=${BINDIR}/BLENDSUR_cy40t1
export PROGRIDBIN=${BINDIR}/cy40t1_PROGRID
#####################################################

####################Climfiles########################
export CLIMFILENAME_ECMWF_LAE=${CLIMDIR}/clim_ecmwf_m
export CLIMFILENAME_ECMWF_GLO=${CLIMDIR}/const.clim_
export CLIMFILENAME_AROME=${CLIMDIR}/clim_arome_oper_new_m
export PGDFILE_LFI=${CLIMDIR}/PGD_SHe20Yr02500_589x421.lfi_sha
export ECOCLIMAPI=${CLIMDIR}/ecoclimapI_covers_param.bin
export ECOCLIMAPII=${CLIMDIR}/ecoclimapII_eu_covers_param.bin
export CLIMFILENAME_BATOR=${CLIMDIR}/param_bator.cfg_cy40t1
export GRIBTABLES=${CLIMDIR}/GRIBTABLES/gribtables
export GRIBTEMPLATES=${CLIMDIR}/GRIBTABLES/gribtemplates
export VARBCFILE=${CLIMDIR}/VARBC.cycle
export BMATRIXFILE1=${BMATRIXDIR}/stabfiltn14.bal
export BMATRIXFILE2=${BMATRIXDIR}/stabfiltn14.cv
export BMATRIXFILE3=${BMATRIXDIR}/stabfiltn14.cvt
export VMATRIXFILE_f=${VMATRIXDIR}/V_forecast_6h_GLdef/stabfiltn42.cvt
export VMATRIXFILE_a=${VMATRIXDIR}/V_analysis_GLdef/stabfiltn42.cvt
#######################################################
