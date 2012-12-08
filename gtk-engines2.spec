%define pkgname gtk-engines
%define pkgversion 2
%define libname %mklibname %{name}

%define cleanice_version 2.4.0
%define bluecurve_version 1.0.0
%define mist_version 0.5

%define gtkbinaryver %(if $([ -x %{_bindir}/pkg-config ] && pkg-config --exists gtk+-2.0); then pkg-config --variable=gtk_binary_version gtk+-2.0; else echo 0; fi)

Name:		%{pkgname}%{pkgversion}
Summary:	Default GTK+ 2.0 theme engines
Version:	2.20.2
Release:	6
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		ftp://ftp.gnome.org/pub/GNOME/sources/gtk-engines/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtk-engines/%{pkgname}-%{version}.tar.bz2
Source3:	http://prdownloads.sourceforge.net/elysium-project/gtk-engines-cleanice-%{cleanice_version}.tar.bz2
Source5:	http://themes.freshmeat.net/redir/gtk2flat/31385/url_tgz/gtk2flat-default.tar.bz2
Source7:	bluecurve-gtk-themes-%{bluecurve_version}.tar.bz2
Patch0:		gtk-engines-2.20.2_glib2.32.patch

BuildRequires:	intltool
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(lua)
Requires:	%{libname} >= %{version}

%description
These are the graphical engines for the various GTK+ toolkit themes.
Included themes are:

  - Notif
  - Redmond95
  - Pixmap
  - Metal (swing-like)
  - Many more

%package -n %{libname}
Summary:	Library files for %{name}
Group:		System/Libraries
Requires:	gtk+2.0 >= 2.9.0

%description -n %{libname}
Library files for %{name}

%package devel
Summary:	Pkgconfig file for %{name}
Group:		Development/Other
Requires:	%{name} >= %{version}

%description devel
Pkgconfig file for %{name}

%prep
%setup -qn %{pkgname}-%{version} -a 3 -a 5 -a 7
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--enable-lua \
	--with-system-lua \
	--enable-animation

%make LIBS=-lm

cd gtk-engines-cleanice-%{cleanice_version}/
libtoolize --copy --force
aclocal
autoconf
autoreconf -fi
%configure2_5x \
	--disable-static
%make
cd ..

cd gtk-flat-theme-2.0/
autoreconf -fi
%configure2_5x \
	--disable-static
%make libflat_la_LIBADD="-lgtk-x11-2.0 -lgdk-x11-2.0 -lgobject-2.0 -lglib-2.0"
cd ..

cd bluecurve-gtk-themes-%{bluecurve_version}/
%configure2_5x \
	--disable-static
%make
cd ..

%install
%makeinstall_std

cd gtk-engines-cleanice-%{cleanice_version}/
%makeinstall_std
cd ..

cd gtk-flat-theme-2.0/
%makeinstall_std libflat_la_LIBADD="-lgtk-x11-2.0 -lgdk-x11-2.0 -lgobject-2.0 -lglib-2.0"
cd ..

cd bluecurve-gtk-themes-%{bluecurve_version}/
%makeinstall_std
cd ..

#remove empty files
rm -f %{buildroot}%{_datadir}/themes/*/ICON.png \
  %{buildroot}%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/*.la \
  %{buildroot}%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/*.a

#gw needed at build time only
rm -rf %{buildroot}%{_datadir}/locale


%files
%doc COPYING README
%{_datadir}/themes/*
%{_datadir}/gtk-engines/

%files -n %{libname}
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libbluecurve.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libcleanice.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libclearlooks.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libcrux-engine.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libflat.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libglide.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libhcengine.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libindustrial.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libluaengine.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libmist.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libredmond95.so
%{_libdir}/gtk-2.0/%{gtkbinaryver}/engines/libthinice.so

%files devel
%{_libdir}/pkgconfig/*


%changelog
* Sat Jun 02 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.20.2-6
+ Revision: 802063
- rebuild creating devel pkg
- pkgconfig file needed for mate-themes

* Fri May 18 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.20.2-5
+ Revision: 799547
- rebuild removing pkgconfig file
- cleaned up spec

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - yearly rebuild
    - yearly rebuild

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.20.2-2
+ Revision: 664943
- mass rebuild

* Fri Oct 01 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.2-1mdv2011.0
+ Revision: 582372
- update to new version 2.20.2

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.20.1-2mdv2010.1
+ Revision: 539614
- rebuild so that shared libraries are properly stripped again

* Sat Apr 17 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.1-1mdv2010.1
+ Revision: 535891
- update to new version 2.20.1

* Tue Mar 30 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.20.0-1mdv2010.1
+ Revision: 528952
- update to new version 2.20.0

* Mon Jan 11 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.19.0-1mdv2010.1
+ Revision: 489955
- update to new version 2.19.0

* Fri Jan 01 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.5-1mdv2010.1
+ Revision: 484676
- update to new version 2.18.5

* Thu Sep 24 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.4-1mdv2010.0
+ Revision: 448383
- update to new version 2.18.4

* Mon Sep 21 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.3-1mdv2010.0
+ Revision: 446956
- build with system lua
- update to new version 2.18.3

* Mon May 18 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.2-1mdv2010.0
+ Revision: 377376
- update to new version 2.18.2

* Sat May 16 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.18.1-2mdv2010.0
+ Revision: 376406
- split gtk-xfce-engine to a standalone package

* Tue Apr 14 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.1-1mdv2009.1
+ Revision: 366933
- update to new version 2.18.1

* Mon Mar 16 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.18.0-1mdv2009.1
+ Revision: 356195
- update to new version 2.18.0

* Mon Mar 02 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.4-1mdv2009.1
+ Revision: 347591
- update to new version 2.17.4

* Fri Feb 27 2009 JÃ©rÃ´me Soyer <saispo@mandriva.org> 2.17.3-2mdv2009.1
+ Revision: 345647
- Update Xfce engine

* Tue Feb 17 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.3-1mdv2009.1
+ Revision: 341296
- fix build
- update to new version 2.17.3

* Sun Dec 07 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.2-1mdv2009.1
+ Revision: 311646
- update to new version 2.17.2

* Tue Dec 02 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.1-1mdv2009.1
+ Revision: 309079
- update to new version 2.17.1

* Tue Nov 04 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.17.0-1mdv2009.1
+ Revision: 299719
- update to new version 2.17.0

* Tue Oct 21 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.1-1mdv2009.1
+ Revision: 295911
- update to new version 2.16.1

* Fri Oct 17 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.16.0-2mdv2009.1
+ Revision: 294766
- update gtk-xfce-engine to the latest version 2.5.91 (Xfce4.6 beta1)

* Mon Sep 22 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.16.0-1mdv2009.0
+ Revision: 286919
- new version

* Tue Sep 02 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.4-1mdv2009.0
+ Revision: 278812
- new version

* Tue Aug 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.3-1mdv2009.0
+ Revision: 273590
- new version

* Tue Aug 05 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.2-1mdv2009.0
+ Revision: 263725
- new version
- update file list, the smooth engine is gone

* Thu Jul 03 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.15.1-1mdv2009.0
+ Revision: 231029
- fix installation
- new version

* Tue Jul 01 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.3-1mdv2009.0
+ Revision: 230455
- new version
- update license

* Tue May 27 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.2-1mdv2009.0
+ Revision: 211689
- more build fixes
- fix buildrequires
- new version
- fix flat theme build

* Wed Apr 09 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.1-1mdv2009.0
+ Revision: 192478
- new version

* Mon Mar 10 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.0-1mdv2008.1
+ Revision: 183799
- new version

* Tue Feb 26 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.6-1mdv2008.1
+ Revision: 175275
- new version

* Tue Feb 12 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.5-1mdv2008.1
+ Revision: 165699
- new version

* Mon Jan 28 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.4-1mdv2008.1
+ Revision: 159482
- new version

* Tue Jan 08 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.3-3mdv2008.1
+ Revision: 146804
- fix cleanice build on x86_64
- replace wonderland by bluecurve gtk engine

* Tue Jan 08 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.3-1mdv2008.1
+ Revision: 146370
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Mon Dec 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.2-1mdv2008.1
+ Revision: 131634
- new version

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - do not package big ChangeLog

* Tue Dec 04 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.1-1mdv2008.1
+ Revision: 115242
- new version

* Sun Nov 18 2007 JÃ©rÃ´me Soyer <saispo@mandriva.org> 2.13.0-2mdv2008.1
+ Revision: 110064
- Add new gtk-xfce-engine

* Wed Nov 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.0-1mdv2008.1
+ Revision: 108582
- new version

* Tue Oct 16 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.12.2-1mdv2008.1
+ Revision: 98886
- new version

* Fri Sep 21 2007 Frederic Crozat <fcrozat@mandriva.com> 2.12.1-1mdv2008.0
+ Revision: 91895
- Release 2.12.1

* Mon Sep 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.12.0-1mdv2008.0
+ Revision: 89346
- new version

* Fri Aug 24 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.11.7-1mdv2008.0
+ Revision: 70982
- new version

* Fri Aug 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.11.6-1mdv2008.0
+ Revision: 64704
- new version

* Tue Aug 14 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.11.5-1mdv2008.0
+ Revision: 63078
- new version

* Tue Aug 07 2007 Frederic Crozat <fcrozat@mandriva.com> 2.11.4-2mdv2008.0
+ Revision: 59863
- Enable animation support in clearlooks engine (Mdv bug #30574)

* Tue Jul 31 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.11.4-1mdv2008.0
+ Revision: 56958
- new version

* Tue Jul 10 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.11.3-1mdv2008.0
+ Revision: 50853
- new version

* Tue Jun 19 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.11.2-1mdv2008.0
+ Revision: 41285
- new version

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 2.11.1-3mdv2008.0
+ Revision: 36283
- rebuild with correct optflags

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - new version

* Tue May 29 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.10.2-1mdv2008.0
+ Revision: 32363
- new version

* Wed Apr 25 2007 JÃ©rÃ´me Soyer <saispo@mandriva.org> 2.10.1-2mdv2008.0
+ Revision: 18148
- Update gtk-engine for the new XFCE

* Wed Apr 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.10.1-1mdv2008.0
+ Revision: 14415
- new version


* Mon Mar 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.10.0-3mdv2007.1
+ Revision: 146579
- package smaller NEWS instead of BIG less usefull ChangeLog

* Tue Mar 13 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.10.0-2mdv2007.1
+ Revision: 142335
- fix buildrequires
- new version
- update file list

* Wed Mar 07 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.9.4-2mdv2007.1
+ Revision: 134510
- fix wrongly requiring devel packages (#29034)

* Tue Feb 27 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.4-1mdv2007.1
+ Revision: 126213
- new version

* Mon Feb 26 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.3-2mdv2007.1
+ Revision: 125756
- fix checkbox colour in clearlooks engine

* Tue Feb 13 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.3-1mdv2007.1
+ Revision: 120273
- new version

* Tue Jan 23 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.2-2mdv2007.1
+ Revision: 112338
- xfce engine 4.4.0

* Mon Jan 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.2-1mdv2007.1
+ Revision: 111970
- new version

* Tue Jan 09 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.1-1mdv2007.1
+ Revision: 106283
- new version
- enable lua engine

* Wed Dec 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.0-3mdv2007.1
+ Revision: 96467
- remove ldconfig calls

* Wed Dec 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.0-2mdv2007.1
+ Revision: 96222
- update xfce engine

  + Colin Guthrie <cguthrie@mandriva.org>
    - Remove the old source tarball

* Tue Dec 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.9.0-1mdv2007.1
+ Revision: 90678
- new version

* Fri Nov 24 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.8.2-2mdv2007.1
+ Revision: 86903
- add conflict to ease upgrade

* Wed Nov 22 2006 Colin Guthrie <cguthrie@mandriva.org> 2.8.2-1mdv2007.1
+ Revision: 86241
- Move the gtk requires to the lib package where it is more appropriate
- Libify the engines for the benefit of x86_64 users

  + GÃ¶tz Waschk <waschk@mandriva.org>
    - new version
    - fix gtkbinaryver macro
    - Import gtk-engines2

* Wed Oct 04 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.8.1-1mdv2007.0
- New version 2.8.1

* Sat Sep 09 2006 Götz Waschk <waschk@mandriva.org> 2.8.0-2mdv2007.0
- obsolete the gtk-xfce-engine package
- update xfce engine

* Wed Sep 06 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.8.0-1mdv2007.0
- New version 2.8.0

* Fri Aug 25 2006 Götz Waschk <waschk@mandriva.org> 2.7.8-2mdv2007.0
- drop bad patch

* Wed Aug 23 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.7.8-1mdv2007.0
- New release 2.7.8

* Wed Aug 09 2006 Götz Waschk <waschk@mandriva.org> 2.7.7-1mdv2007.0
- rediff the patch
- New release 2.7.7

* Wed Jul 26 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.7.6-1mdv2007.0
- New release 2.7.6

* Wed Jul 12 2006 Götz Waschk <waschk@mandriva.org> 2.7.5-1mdv2007.0
- drop patches 0,1
- New release 2.7.5

* Fri Jun 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.7.4-1mdv2007.0
- Release 2.7.4
- Patches 0, 1, 2 : fixes from Fedora

* Wed May 31 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.9-1mdv2007.0
- New release 2.6.9

* Mon Mar 13 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.8-1mdk
- New release 2.6.8

* Mon Jan 09 2006 Götz Waschk <waschk@mandriva.org> 2.6.7-1mdk
- drop patch
- New release 2.6.7
- use mkrel

* Mon Dec 05 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.6-2mdk
- Patch0 (CVS): remove undefined reference

* Tue Nov 29 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.6-1mdk
- New release 2.6.6

* Sat Sep 03 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.5-2mdk
- rebuild to remove glitz dep

* Thu Aug 25 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.6.5-1mdk
- New release 2.6.5

* Fri Jul 29 2005 Götz Waschk <waschk@mandriva.org> 2.6.4-1mdk
- install fix
- New release 2.6.4

* Tue May 10 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.3-1mdk 
- fix build on x86-64

* Tue Apr 19 2005 Frederic Crozat <fcrozat@mandriva.com> 2.6.3-1mdk 
- Release 2.6.3 based on GÃ¶tz Waschk package
- Update cleanice to 2.4.0 and its url

* Mon Mar 14 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.2-2mdk 
- Add conflicts to easy upgrade

* Tue Mar 08 2005 GÃ¶tz Waschk <waschk@linux-mandrake.com> 2.6.2-1mdk
- New release 2.6.2

* Thu Feb 10 2005 Götz Waschk <waschk@linux-mandrake.com> 2.6.1-1mdk
- update the file list
- New release 2.6.1

* Mon Jan 10 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.6.0-4mdk 
- fix x86_64 build

* Fri Jan 07 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.6.0-3mdk 
- buildrequires

* Tue Dec 28 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.6.0-2mdk 
- Add conflicts with old version of ximian-artwork and gnome-themes

* Mon Dec 27 2004 Götz Waschk <waschk@linux-mandrake.com> 2.6.0-1mdk
- update file list
- add source URL
- New release 2.6.0

* Fri Dec 17 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2.0-8mdk
- Don't ship pixmap engine, it is now part of GTK+ 2.6

* Wed Nov 10 2004 Götz Waschk <waschk@linux-mandrake.com> 2.2.0-7mdk
- new xfce engine 2.2.1

* Sun Apr 04 2004 Götz Waschk <waschk@linux-mandrake.com> 2.2.0-6mdk
- rebuild for new gtk

