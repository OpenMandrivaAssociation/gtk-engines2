%define pkgname gtk-engines
%define pkgversion 2
%define libname %mklibname %{name}

%define cleanice_version 2.4.0
%define bluecurve_version 1.0.0
%define mist_version 0.5

%define gtkbinaryver %(if $([ -x %{_bindir}/pkg-config ] && pkg-config --exists gtk+-2.0); then pkg-config --variable=gtk_binary_version gtk+-2.0; else echo 0; fi)

Summary:	Default GTK+ 2.0 theme engines
Name:		%{pkgname}%{pkgversion}
Version:	2.20.2
Release:	9
License:	GPLv2+ and LGPLv2+
Group:		System/Libraries
Url:		ftp://ftp.gnome.org/pub/GNOME/sources/gtk-engines/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtk-engines/%{pkgname}-%{version}.tar.bz2
Source3:	http://prdownloads.sourceforge.net/elysium-project/gtk-engines-cleanice-%{cleanice_version}.tar.bz2
Source5:	http://themes.freshmeat.net/redir/gtk2flat/31385/url_tgz/gtk2flat-default.tar.bz2
Source7:	bluecurve-gtk-themes-%{bluecurve_version}.tar.bz2
Patch0:		gtk-engines-2.20.2_glib2.32.patch
Patch1:		gtk-engines-automake-1.13.patch

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

