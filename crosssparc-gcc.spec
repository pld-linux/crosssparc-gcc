Summary:	Cross SPARC GNU binary utility development utilities - gcc
Summary(es.UTF-8):   Utilitarios para desarrollo de binarios de la GNU - SPARC gcc
Summary(fr.UTF-8):   Utilitaires de développement binaire de GNU - SPARC gcc
Summary(pl.UTF-8):   Skrośne narzędzia programistyczne GNU dla SPARC - gcc
Summary(pt_BR.UTF-8):   Utilitários para desenvolvimento de binários da GNU - SPARC gcc
Summary(tr.UTF-8):   GNU geliştirme araçları - SPARC gcc
Name:		crosssparc-gcc
Version:	3.4.0
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	85c6fc83d51be0fbb4f8205accbaff59
Patch1:		crosssparc-gcc-3.4.0-include-fix.patch
BuildRequires:	crosssparc-binutils
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	autoconf
BuildRequires:	/bin/bash
Requires:	crosssparc-binutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cxx		0
%define		target		sparc-pld-linux
%define		_prefix		/usr
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc/%{target}
%define		gcclib		%{_prefix}/lib/gcc/%{target}/%{version}

%define		_noautostrip	.*libgcc\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on SPARC linux (architecture sparc-linux) on
i386-machines.

%description -l de.UTF-8
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
i386-Rechner Code für sparc-Linux zu generieren.

%description -l pl.UTF-8
Ten pakiet zawiera skrośny gcc pozwalający na robienie na maszynach
i386 binariów do uruchamiania na SPARC (architektura "sparc-linux").

%prep
%setup -q -n gcc-%{version}
%patch1 -p1

%build
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false ../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--disable-shared \
	--enable-haifa \
	--enable-languages="c" \
	--enable-long-long \
	--enable-namespaces \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-x \
	--target=%{target}

PATH=$PATH:/sbin:%{_sbindir}

cd ..
#LDFLAGS_FOR_TARGET="%{rpmldflags}"

%{__make} -C obj-%{target}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_datadir},%{_bindir},%{gcclib}}

cd obj-%{target}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} -C gcc install \
	prefix=%{_prefix} \
	mandir=%{_mandir} \
	infodir=%{_infodir} \
	gxx_include_dir=$RPM_BUILD_ROOT%{arch}/include/g++ \
	DESTDIR=$RPM_BUILD_ROOT

# c++filt is provided by binutils
#rm -f $RPM_BUILD_ROOT%{_bindir}/i386-mipsel-c++filt

# what is this there for???
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# the same... make hardlink
#ln -f $RPM_BUILD_ROOT%{arch}/bin/gcc $RPM_BUILD_ROOT%{_bindir}/%{target}-gcc

%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-cpp
#%dir %{arch}/bin
#%attr(755,root,root) %{arch}/bin/cpp
#%attr(755,root,root) %{arch}/bin/gcc
#%attr(755,root,root) %{arch}/bin/gcov
#%%{arch}/include/_G_config.h
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
##%attr(755,root,root) %{gcclib}/tradcpp0
##%attr(755,root,root) %{gcclib}/cpp0
%attr(755,root,root) %{gcclib}/collect2
#%%{gcclib}/SYSCALLS.c.X
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
#%%{gcclib}/include/iso646.h
#%%{gcclib}/include/limits.h
#%%{gcclib}/include/proto.h
#%%{gcclib}/include/stdarg.h
#%%{gcclib}/include/stdbool.h
#%%{gcclib}/include/stddef.h
#%%{gcclib}/include/syslimits.h
#%%{gcclib}/include/varargs.h
#%%{gcclib}/include/va-*.h
%{_mandir}/man1/%{target}-gcc.1*
