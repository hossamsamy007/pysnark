# Copyright (c) 2016-2018 Koninklijke Philips N.V. All rights reserved. A
# copyright license for redistribution and use in source and binary forms,
# with or without modification, is hereby granted for non-commercial,
# experimental and research purposes, provided that the following conditions
# are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimers.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimers in the
#   documentation and/or other materials provided with the distribution. If
#   you wish to use this software commercially, kindly contact
#   info.licensing@philips.com to obtain a commercial license.
#
# This license extends only to copyright and does not include or grant any
# patent license or other license whatsoever.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import os.path
import subprocess
import random
import sys

import options
import qaptools.runqapgen

if __name__ == "__main__":
    if len(sys.argv)<2:
        print >>sys.stderr, "*** Usage:", sys.argv[0], "<bname> [values]"
        sys.exit(2)

    bn = sys.argv[1]

    bf = options.get_block_file(bn)
    bfile = open(bf, "w")

    bc = options.get_block_comm(bn)

    print >>sys.stderr, "Writing block", bn, "to", bf, "+", bc

    nvals = 0

    if len(sys.argv)==2:
        for ln in sys.stdin:
            vals = map(int, ln.strip().split())
            for val in vals:
                print >>bfile, val
                nvals += 1
    else:
        for val in sys.argv[2:]:
            print >>bfile, int(val)
            nvals += 1

    print >>bfile, random.SystemRandom().randint(0, options.vc_p-1)
    bfile.close()

    qaptools.runqapgen.ensure_mkey(-1, nvals)

    outf = open(bc, "w")
    ret = subprocess.call([options.get_qaptool_exe("qapinput"), options.get_mpkey_file(), bf], stdout=outf)
    outf.close()
    if ret != 0: sys.exit(2)