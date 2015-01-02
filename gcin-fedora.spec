Name:           gcin
Version:        2.8.2
Release:        liu%{?dist}
Summary:        Input method for Traditional Chinese

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://cle.linux.org.tw/gcin/
##Got a request to get new gcin source from the following link
##original source url is not opening since last few months.
Source0:        http://www.csie.nctu.edu.tw/~cp76/gcin/download/%{name}-%{version}.tar.xz
#Source0:        %{name}-%{version}.tar.xz
Source1:        gcin.conf

BuildRequires:  qt-devel, gtk3-devel, gtk2-devel, desktop-file-utils
BuildRequires:  libXtst-devel
BuildRequires:  anthy-devel
Requires:       im-chooser, imsettings, gcin-gtk2
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives

%description
Gcin is an input method for Traditional Chinese with a GTK user interface.

%package im_client
Summary: gcin im client library 
Group:  Applications/System
Requires: gtk2
Requires: %{name} = %{version}-%{release}

%description im_client
gcin im client

%package gtk2
Summary: Gtk2 support for gcin
Group:  Applications/System
Requires: gtk2 gcin-im_client
Requires: %{name} = %{version}-%{release}

%description gtk2
gtk2 support for gcin.

%package gtk3
Summary: Gtk3 support for gcin
Group:  Applications/System
Requires: gtk3 gcin-im_client
Requires: %{name} = %{version}-%{release}

%description gtk3
gtk3 support for gcin.

%package qt4
Summary: Qt support for gcin
Group:   Applications/System
Requires: qt4 gcin-im_client
Requires: %{name} = %{version}-%{release}

%description qt4
qt4 support for gcin.

%prep
%setup -q
sed -i.strip -e 's|install[ \t][ \t]*-s|install|' Makefile

%build
%configure
perl -pi -e "s/^(OPTFLAGS.*=)/\1 %{optflags} /" config.mak
# fixme: explain how %%{?_smp_mflags} breaks build?
make

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit/xinput.d
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit/xinput.d/gcin.conf
# devel files {
rm -f $RPM_BUILD_ROOT/%{_includedir}/gcin-im-client.h
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgcin-im-client.so
# }
rm -f $RPM_BUILD_ROOT/%{_docdir}/gcin-%{version}/Changelog
rm -f $RPM_BUILD_ROOT/%{_docdir}/gcin-%{version}/README
desktop-file-install \
  --delete-original \
  --vendor fedora \
  --dir ${RPM_BUILD_ROOT}/%{_datadir}/applications \
  --add-category X-Fedora \
  ${RPM_BUILD_ROOT}/%{_datadir}/applications/gcin-tools.desktop

%post
/sbin/ldconfig
update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || :
%{_sbindir}/alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_sysconfdir}/X11/xinit/xinput.d/gcin.conf 40

%post gtk2
if [ $1 -eq 1 ] ; then
    # For upgrades, the cache will be regenerated by the new package's %%postun
    gtk-query-immodules-2.0-%{__isa_bits} > /etc/gtk-2.0/%{_arch}-redhat-linux-gnu/gtk.immodules || :
fi

%post gtk3
if [ $1 -eq 1 ] ; then
    # For upgrades, the cache will be regenerated by the new package's %%postun
    gtk-query-immodules-3.0-%{__isa_bits} --update-cache &> /dev/null || :
fi

%postun
/sbin/ldconfig
update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || :

%postun gtk2
gtk-query-immodules-2.0-%{__isa_bits} > /etc/gtk-2.0/%{_arch}-redhat-linux-gnu/gtk.immodules || :

%postun gtk3
gtk-query-immodules-3.0-%{__isa_bits} --update-cache &> /dev/null || :

%preun
if [ $1 -eq 0 ]; then
    %{_sbindir}/alternatives --remove xinputrc %{_sysconfdir}/X11/xinit/xinput.d/gcin.conf >/dev/null 2>&1 || :
fi

%files
%doc AUTHORS COPYING Changelog.html README.html
%config %{_sysconfdir}/X11/xinit/xinput.d/gcin.conf
%{_bindir}/gcin*
%{_bindir}/gtab*
%{_bindir}/juyin-learn
%{_bindir}/pho*
%{_bindir}/sim2trad
%{_bindir}/trad2sim
%{_bindir}/ts*
%{_bindir}/txt2gtab-phrase
%{_datadir}/applications/fedora-gcin-tools.desktop
%{_datadir}/gcin/
%{_datadir}/icons/*
%{_libdir}/gcin/*module.so
%{_libdir}/gcin/gcin*.so

%files im_client
%{_libdir}/gcin/libgcin*.so*

%files gtk2
%{_libdir}/gtk-2.0/immodules/im-gcin.so

%files gtk3
%{_libdir}/gtk-3.0/immodules/im-gcin.so

%files qt4
%{_libdir}/qt4/plugins/inputmethods/im-gcin.so

%changelog
* Tue Dec 12 2011 Edward Liu - 2.5.1
* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.6.1-2
- Rebuild for new libpng

* Tue May 03 2011 Parag Nemade <paragn AT fedoraproject.org> - 1.6.1-1
- update to latest stable release 1.6.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.5.5-4
- Resolves:rh#660992-FTBFS gcin-1.5.5-3.fc15

* Tue Sep 07 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.5.5-3
- update to latest stable release 1.5.5
- Fix gtk-im module Makefile issue

* Tue Jun 29 2010 Chung-Yen Chang <candyz0416@gmail.com> - 1.5.5.pre3-2
- update to 1.5.5.pre3

* Wed Jun 23 2010 Chung-Yen Chang <candyz0416@gmail.com> - 1.5.1-1
- update to 1.5.1

* Wed Jun 23 2010 Chung-Yen Chang <candyz0416@gmail.com> - 1.5.0-2
- update to 1.5.0

* Wed Jun 23 2010 Chung-Yen Chang <candyz0416@gmail.com> - 1.5.0-1
- update to 1.5.0

* Wed May 05 2010 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.6-2
- patch to add -lm to LDFLAGS
- patch to stop using GTK+ deprecated AP

* Tue Jan 05 2010 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.6-1
- update to 1.4.6

* Fri Nov 27 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.5-6
- fix No icon for im-chooser (#468829)

* Tue Nov 24 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.5-5
- fix No icon for im-chooser (#468829)

* Mon Nov 16 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.5-4
- Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 07 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.5-2
- remove gtk_bug_fix.so and rebuild

* Thu May 07 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.5-1
- update to 1.4.5

* Tue Mar 31 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.4.4-5
- fix unowned directory (#473616)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.4-3
- rename Changelog to Changelog.html

* Wed Feb 04 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.4-2
- rename README to README.html

* Wed Feb 04 2009 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.4-1
- update to 1.4.4

* Tue Oct 21 2008 Jens Petersen <petersen@redhat.com> - 1.4.2-4
- add gcin-1.4.2-gtk-immodules-lang.patch to not enable gcin gtk immodule for all
  langs (#453093)
- spec file cleanup
- update xinput conf file to set icon and setup program (#456512)

* Mon Sep 29 2008 Jens Petersen <petersen@redhat.com> - 1.4.2-3
- update im-client.patch to fix patch fuzz

* Fri Jun 27 2008 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.2-2
- update gcin.conf (change gcin to /usr/bin/gcin)
- add imsettings to Requires
- fix bug #453085

* Thu Jun 26 2008 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.2-1
- update to 1.4.2

* Fri Jun 20 2008 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.1-1
- update to 1.4.1

* Wed May 21 2008 Chung-Yen Chang <candyz0416@gmail.com> - 1.4.0-1
- update to 1.4.0

* Sat May 17 2008 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.9-3
- add /bin/sh /bin/bash to requires

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.9-2
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.9-1
- update to 1.3.9

* Wed Jan 23 2008 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.8-1
- update to 1.3.8

* Tue Nov 27 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.7.1-1
- update to 1.3.7.1

* Mon Oct 15 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.5-2
- update im-client.patch and newcj3.patch

* Sun Oct 14 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.5-1
- update to 1.3.5

* Thu Sep 20 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.4-3
- update license field to LGPLv2
- add im-chooser to require

* Tue Apr 17 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.4-2
- disable i18n and do not make po

* Tue Apr 17 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.4-1
- update to 1.3.4

* Tue Jan 30 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.3-1
- update to 1.3.3

* Mon Jan 01 2007 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.2-1
- update to 1.3.2

* Sun Dec 03 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.1-1
- update to 1.3.1

* Thu Nov 23 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.0.1-2
- rebuild

* Thu Nov 23 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.3.0.1-1
- update to 1.3.0.1

* Fri Nov 17 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.9-3
- add gcin129update.patch

* Fri Nov 17 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.9-2
- update NewCJ3.cin

* Wed Nov 15 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.9-1
- update to 1.2.9
- add NewCJ3.cin

* Fri Oct 20 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.8-1
- update to 1.2.8

* Mon Oct 09 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.7-1
 - update to 1.2.7

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.2.6-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.6-1
- update to 1.2.6

* Fri Sep 15 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.5-2
- rebuild

* Fri Sep 08 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.5-1
- update to 1.2.5
- add icons

* Tue Sep 05 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.4-1
- update to 1.2.4

* Fri Sep 01 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.3-3
- make tag and make build again

* Fri Sep 01 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.3-2
- make new-sources to upload new source tarball

* Fri Sep 01 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.3-1
- update to 1.2.3

* Tue Aug 29 2006 Chung-Yen Chang <candyz0416@gmail.com> - 1.2.2-13
- typo fix

* Thu Aug 24 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-12
- modify spec file only for fc5 and later (branch the spec file)

* Thu Aug 24 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-11
- fix to handle fedora tag correctly

* Thu Aug 24 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-10
- Remove patch5 (not necessary)

* Wed Aug 23 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-9
- Fix patch5 for fc3 only bug

* Sun Aug 20 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-8
- Fix changelog

* Sun Aug 20 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-7
- Remove -devel subpackage
- install desktop file

* Sat Aug 19 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-6
- a few more fixes from Jens Petersen

* Sat Aug 19 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-5
- improvements from Jens Petersen:
- don't use configure macro
- add .conf suffix to xinput.d file and update install scripts for fc6
- move lib to libdir and drop ld.so.conf.d file
- other minor cleanup

* Sat Aug 19 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-4
- rebuild 1.2.2-4

* Fri Aug 18 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-3
- Add COPYING Changelog to doc
- Use Dist Tag

* Fri Aug 18 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-2
- fix x86_64 problems

* Tue Aug 17 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.2-1
- rebuild 1.2.2-1

* Tue Aug 17 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.1-7
- rebuild 1.2.1-7

* Wed Aug 16 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.1-4
- rebuild 1.2.1-4

* Thu Jul 13 2006 Chung-Yen Chang <candyz@cle.linux.org.tw> - 1.2.1-1
- update to 1.2.1

* Mon May 08 2006 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.2.0

* Mon May 01 2006 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.9

* Mon Apr 03 2006 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.8

* Wed Mar 29 2006 Chung-Yen Chang <candyz@cle.linux.org.tw>
- rebuild for FC5

* Wed Feb 22 2006 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.7

* Thu Feb 02 2006 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.6

* Sat Jan 07 2006 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.5

* Mon Dec 19 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.4-2

* Mon Dec 12 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.4

* Mon Nov 21 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.3

* Tue Nov 08 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.2

* Sun Oct 30 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.1

* Mon Oct 24 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.1.0

* Mon Oct 03 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.9

* Mon Sep 26 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.8

* Mon Sep 19 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.7

* Mon Sep 05 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.4

* Mon Aug 22 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.3

* Wed Aug 10 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.2

* Fri Jul 08 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.1

* Mon Jun 27 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 1.0.0

* Thu Jun 23 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.9

* Thu Jun 16 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- rebuild for fc4

* Tue May 31 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.7

* Tue May 19 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.6

* Tue May 12 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.5

* Wed May 04 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.3

* Mon Apr 25 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- fix alternatives

* Fri Apr 22 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.2

* Sat Apr 16 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.1

* Tue Apr 05 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.9.0

* Tue Mar 22 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.8.9

* Sat Mar 14 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.8.8

* Sat Mar 08 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.8.7

* Sat Mar 05 2005 Chung-Yen Chang <candyz@cle.linux.org.tw>
- update to 0.8.6

* Mon Aug 23 2004 Chung-Yen Chang <candyz@cle.linux.org.tw>
- frist build for Fedora Core 2
