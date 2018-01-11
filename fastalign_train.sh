FASTALIGN="/disk/ocean/public/tools/fast_align/build"

${FASTALIGN}/fast_align -i $1 -d -o -v -p $2/fwd_params > $2/forward.align 2>$2/fwd_err
${FASTALIGN}/fast_align -i $1 -d -o -v -r -p $2/rev_params > $2/reverse.align 2>$2/rev_err
