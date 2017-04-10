FASTALIGN="/disk/ocean/public/tools/fast_align/build"
resources="resources_zh"

${FASTALIGN}/fast_align -i $1 -d -o -v -p $resources/fwd_params > $resources/forward.align 2>$resources/fwd_err
${FASTALIGN}/fast_align -i $1 -d -o -v -r -p $resources/rev_params > $resources/reverse.align 2>$resources/rev_err
