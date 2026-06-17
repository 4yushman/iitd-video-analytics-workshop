```text
Script started on 2026-06-17 16:03:14+05:30 [TERM="xterm-256color" TTY="/dev/pts/3" COLUMNS="184" LINES="42"]
]0;ayush-ubantu@Ayush-Ubantu: ~/Desktop/iit-video-analytics-workshopayush-ubantu@Ayush-Ubantu:~/Desktop/iit-video-analytics-workshop$ docker start 578a3f0a8b4edocker start 578a3f0a8b4e

578a3f0a8b4e
]0;ayush-ubantu@Ayush-Ubantu: ~/Desktop/iit-video-analytics-workshopayush-ubantu@Ayush-Ubantu:~/Desktop/iit-video-analytics-workshop$ cd /home/ayush-ubantu/Downloads/sample/samplecd /home/ayush-ubantu/Downloads/sample/sample

]0;ayush-ubantu@Ayush-Ubantu: ~/Downloads/sample/sampleayush-ubantu@Ayush-Ubantu:~/Downloads/sample/sample$ mkdir =segments

]0;ayush-ubantu@Ayush-Ubantu: ~/Downloads/sample/sampleayush-ubantu@Ayush-Ubantu:~/Downloads/sample/sample$ ffmpeg -i sample.mp4 -an -c:v libx264 -map 0:v:0 -segment_time 0.5 -reset_timestamps 1 -g 15 -sc_threshold 0 -force_key_frames "expr:gte(t,n_forced*0.5)" -f segment segments/seg_%04d.mp4ffmpeg -i sample.mp4 -an -c:v libx264 -map 0:v:0 -segment_time 0.5 -reset_timestamps 1 -g 15 -sc_threshold 0 -force_key_frames "expr:gte(t,n_forced*0.5)" -f segment segments/seg_%04d.mp4

ffmpeg version 6.1.1-3ubuntu5 Copyright (c) 2000-2023 the FFmpeg developers
  built with gcc 13 (Ubuntu 13.2.0-23ubuntu3)
  configuration: --prefix=/usr --extra-version=3ubuntu5 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --disable-omx --enable-gnutls --enable-libaom --enable-libass --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libglslang --enable-libgme --enable-libgsm --enable-libharfbuzz --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-openal --enable-opencl --enable-opengl --disable-sndio --enable-libvpl --disable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-ladspa --enable-libbluray --enable-libjack --enable-libpulse --enable-librabbitmq --enable-librist --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libx264 --enable-libzmq --enable-libzvbi --enable-lv2 --enable-sdl2 --enable-libplacebo --enable-librav1e --enable-pocketsphinx --enable-librsvg --enable-libjxl --enable-shared
  libavutil      58. 29.100 / 58. 29.100
  libavcodec     60. 31.102 / 60. 31.102
  libavformat    60. 16.100 / 60. 16.100
  libavdevice    60.  3.100 / 60.  3.100
  libavfilter     9. 12.100 /  9. 12.100
  libswscale      7.  5.100 /  7.  5.100
  libswresample   4. 12.100 /  4. 12.100
  libpostproc    57.  3.100 / 57.  3.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'sample.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2mp41
    encoder         : Lavf58.29.100
  Duration: 00:00:03.36, start: 0.000000, bitrate: 3082 kb/s
  Stream #0:0[0x1](und): Video: hevc (Main) (hev1 / 0x31766568), yuvj420p(pc, progressive), 1920x1080, 3072 kb/s, 25 fps, 25 tbr, 12800 tbn (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
Stream mapping:
  Stream #0:0 -> #0:0 (hevc (native) -> h264 (libx264))
Press [q] to stop, [?] for help
[libx264 @ 0x5a00981c6a80] using cpu capabilities: MMX2 SSE2Fast SSSE3 SSE4.2 AVX FMA3 BMI2 AVX2
[libx264 @ 0x5a00981c6a80] profile High, level 4.0, 4:2:0, 8-bit
[libx264 @ 0x5a00981c6a80] 264 - core 164 r3108 31e19f9 - H.264/MPEG-4 AVC codec - Copyleft 2003-2023 - http://www.videolan.org/x264.html - options: cabac=1 ref=3 deblock=1:0:0 analyse=0x3:0x113 me=hex subme=7 psy=1 psy_rd=1.00:0.00 mixed_ref=1 me_range=16 chroma_me=1 trellis=1 8x8dct=1 cqm=0 deadzone=21,11 fast_pskip=1 chroma_qp_offset=-2 threads=12 lookahead_threads=2 sliced_threads=0 nr=0 decimate=1 interlaced=0 bluray_compat=0 constrained_intra=0 bframes=3 b_pyramid=2 b_adapt=1 b_bias=0 direct=1 weightb=1 open_gop=0 weightp=2 keyint=15 keyint_min=1 scenecut=0 intra_refresh=0 rc_lookahead=15 rc=crf mbtree=1 crf=23.0 qcomp=0.60 qpmin=0 qpmax=69 qpstep=4 ip_ratio=1.40 aq=1:1.00
[segment @ 0x5a00981f40c0] Opening 'segments/seg_0000.mp4' for writing
Output #0, segment, to 'segments/seg_%04d.mp4':
  Metadata:
    major_brand     : isom
    minor_version   : 512
    compatible_brands: isomiso2mp41
    encoder         : Lavf60.16.100
  Stream #0:0(und): Video: h264, yuvj420p(pc, progressive), 1920x1080, q=2-31, 25 fps, 12800 tbn (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
      encoder         : Lavc60.31.102 libx264
    Side data:
      cpb: bitrate max/min/avg: 0/0/0 buffer size: 0 vbv_delay: N/A
frame=    0 fps=0.0 q=0.0 size=       0kB time=N/A bitrate=N/A speed=N/A    
frame=    4 fps=0.0 q=28.0 size=N/A time=00:00:00.08 bitrate=N/A speed=0.132x    
[segment @ 0x5a00981f40c0] Opening 'segments/seg_0001.mp4' for writing
[segment @ 0x5a00981f40c0] Opening 'segments/seg_0002.mp4' for writing
[segment @ 0x5a00981f40c0] Opening 'segments/seg_0003.mp4' for writing
frame=   42 fps= 36 q=28.0 size=N/A time=00:00:01.60 bitrate=N/A speed=1.38x    
[segment @ 0x5a00981f40c0] Opening 'segments/seg_0004.mp4' for writing
[segment @ 0x5a00981f40c0] Opening 'segments/seg_0005.mp4' for writing
[segment @ 0x5a00981f40c0] Opening 'segments/seg_0006.mp4' for writing
[out#0/segment @ 0x5a00981c8fc0] video:2360kB audio:0kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: unknown
frame=   84 fps= 50 q=-1.0 Lsize=N/A time=00:00:03.24 bitrate=N/A speed=1.92x    
[libx264 @ 0x5a00981c6a80] frame I:7     Avg QP:18.58  size:129625
[libx264 @ 0x5a00981c6a80] frame P:32    Avg QP:22.43  size: 43371
[libx264 @ 0x5a00981c6a80] frame B:45    Avg QP:25.28  size:  2672
[libx264 @ 0x5a00981c6a80] consecutive B-frames: 20.2% 21.4% 10.7% 47.6%
[libx264 @ 0x5a00981c6a80] mb I  I16..4: 10.9% 77.8% 11.3%
[libx264 @ 0x5a00981c6a80] mb P  I16..4:  1.7%  5.7%  0.7%  P16..4: 22.5% 10.8%  7.4%  0.0%  0.0%    skip:51.1%
[libx264 @ 0x5a00981c6a80] mb B  I16..4:  0.0%  0.1%  0.0%  B16..8: 20.1%  0.6%  0.2%  direct: 0.3%  skip:78.7%  L0:37.8% L1:57.9% BI: 4.3%
[libx264 @ 0x5a00981c6a80] 8x8 transform intra:75.7% inter:87.9%
[libx264 @ 0x5a00981c6a80] coded y,uvDC,uvAC intra: 67.8% 32.2% 5.6% inter: 10.7% 4.9% 0.1%
[libx264 @ 0x5a00981c6a80] i16 v,h,dc,p: 11% 52%  9% 28%
[libx264 @ 0x5a00981c6a80] i8 v,h,dc,ddl,ddr,vr,hd,vl,hu: 19% 37% 18%  4%  3%  3%  5%  3%  8%
[libx264 @ 0x5a00981c6a80] i4 v,h,dc,ddl,ddr,vr,hd,vl,hu: 27% 43%  9%  3%  4%  3%  5%  2%  4%
[libx264 @ 0x5a00981c6a80] i8c dc,h,v,p: 60% 26% 12%  2%
[libx264 @ 0x5a00981c6a80] Weighted P-Frames: Y:6.2% UV:3.1%
[libx264 @ 0x5a00981c6a80] ref P L0: 79.1%  9.5%  7.2%  3.1%  1.2%
[libx264 @ 0x5a00981c6a80] ref B L0: 90.6%  8.7%  0.7%
[libx264 @ 0x5a00981c6a80] ref B L1: 97.6%  2.4%
[libx264 @ 0x5a00981c6a80] kb/s:5751.19
]0;ayush-ubantu@Ayush-Ubantu: ~/Downloads/sample/sampleayush-ubantu@Ayush-Ubantu:~/Downloads/sample/sample$ rm -rf /home/ayush-ubantu/Downloads/sample/sample/segments
rm -rf /home/ayush-ubantu/Downloads/sample/sample/segmenteexit

exit

Script done on 2026-06-17 16:22:02+05:30 [COMMAND_EXIT_CODE="0"]
```
