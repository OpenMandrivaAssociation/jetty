# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global jettyname   jetty
%global jtuid       110
%global username    %{name}
%global confdir     %{_sysconfdir}/%{name}
%global logdir      %{_localstatedir}/log/%{name}
%global homedir     %{_datadir}/%{name}
%global jettycachedir %{_localstatedir}/cache/%{name}
%global tempdir     %{jettycachedir}/temp
%global rundir      %{_localstatedir}/run/%{name}
%global jettylibdir %{_localstatedir}/lib/%{name}
%global appdir      %{jettylibdir}/webapps

Name:           jetty
Version:        6.1.26
Release:        4
Summary:        The Jetty Webserver and Servlet Container

Group:          Development/Java
License:        ASL 2.0
URL:            http://jetty.mortbay.org/jetty/
Source0:        http://dist.codehaus.org/%{name}/%{name}-%{version}/%{name}-%{version}-src.zip
Source1:	djetty.script
Source2:        jetty.init
Source3:        jetty.logrotate
Source4:        %{name}-depmap.xml
Patch0:	        disable-modules.patch
Patch1:	        jetty-util-pom.patch
Patch4:	        jetty-plugin-fix-site.patch
Patch5:	        jetty-6.1.26-CVE-2011-4461.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%{?FE_USERADD_REQ}
BuildRequires:  jpackage-utils >= 0:1.6
# build only
BuildRequires: maven-antrun-plugin
BuildRequires: apache-commons-parent
BuildRequires: maven-compiler-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-site-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-project-info-reports-plugin
BuildRequires: maven-dependency-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-war-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-release-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-shared-dependency-tree
BuildRequires: tomcat6-lib
BuildRequires: servlet25
BuildRequires: jsp21
BuildRequires: slf4j
BuildRequires: objectweb-asm
BuildRequires: apache-commons-el
BuildRequires: apache-commons-daemon
BuildRequires: geronimo-jta
BuildRequires: geronimo-parent-poms
BuildRequires: apache-commons-parent
BuildRequires: derby

Requires:  chkconfig
Requires:  jpackage-utils >= 0:1.6
Requires:  ant >= 0:1.6
Requires:  apache-commons-parent
Requires:  apache-commons-el
Requires:  apache-commons-logging
Requires:  tomcat6-lib >= 6.0.26
Requires:  jsp
Requires:  mx4j >= 0:3.0
Requires: servlet25
Requires: jsp21
Requires: slf4j
Requires: javamail
Requires:  xerces-j2 >= 0:2.7
Requires:  xml-commons-apis
Requires(post): jpackage-utils >= 0:1.6
Requires(postun): jpackage-utils >= 0:1.6
Provides:  group(%username) = %jtuid
Provides:  user(%username) = %jtuid

%description
Jetty is a 100% Java HTTP Server and Servlet Container. 
This means that you do not need to configure and run a 
separate web server (like Apache) in order to use java, 
servlets and JSPs to generate dynamic content. Jetty is 
a fully featured web server for static and dynamic content. 
Unlike separate server/container solutions, this means 
that your web server and web application run in the same 
process, without interconnection overheads and complications. 
Furthermore, as a pure java component, Jetty can be simply 
included in your application for demonstration, distribution 
or deployment. Jetty is available on all Java supported 
platforms.  

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}

%description    manual
%{summary}.

%prep
%setup -q -n %{jettyname}-%{version}
for f in $(find . -name "*.?ar"); do rm $f; done
find . -name "*.class" -exec rm {} \;

%patch0 -p0 -b .sav
%patch1 -p0 -b .sav
%patch4 -p0 -b .sav
%patch5 -p1 -b .CVE-2011-4461

cp %{SOURCE1} djetty

#remove glassfish specific file
rm -fr modules/jsp-2.1/src/main/java/com/sun/org/apache/commons/logging/impl/JettyLog.java

sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/management/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/management/pom.xml
sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/jsp-2.0/pom.xml
sed -i "s|<groupId>ant</groupId>|<groupId>org.apache.ant</groupId>|g" modules/jsp-2.0/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/jsp-2.0/pom.xml
sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/naming/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/naming/pom.xml
sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/annotations/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/annotations/pom.xml

sed -i "s|mvn|mvn-jpp|g" distribution/jetty-assembly/pom.xml

sed -i "s|zip \$D/\$N|zip \$D/\$N/\$N|g" bin/build_release_bundles.sh

sed -i "s|# look for JETTY_HOME|export JETTY_HOME=/usr/share/jetty|g" bin/jetty-xinetd.sh

sed -i "s|jcl104-over-slf4j|slf4j-jcl|g" modules/jsp-2.0/pom.xml 

%build
sed -i -e "s|/usr/share|%{_datadir}|g" djetty

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository

mvn-jpp \
    -e \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    -Dmaven2.jpp.depmap.file=%{SOURCE4} \
    -Dmaven.test.skip=true \
    -DupdateReleaseInfo=true \
    install
    
#pushd distribution/jetty-assembly
#  mvn-jpp \
#       -e \
#       -s $(pwd)/settings.xml \
#       -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
#       -Dmaven2.jpp.depmap.file=%{SOURCE4} \
#       -Dmaven.test.skip=true \
#       install
#popd

sh bin/build_release_bundles.sh .

%install
rm -rf $RPM_BUILD_ROOT
# dirs
install -dm 755 $RPM_BUILD_ROOT%{_bindir}
install -dm 755 $RPM_BUILD_ROOT%{_initrddir}
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP.jetty-jetty.pom
install -pm 644 modules/util/pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP.jetty-jetty-util.pom

%add_to_maven_depmap org.mortbay.jetty jetty %{version} JPP/jetty jetty
%add_to_maven_depmap org.mortbay.jetty jetty-util %{version} JPP/jetty jetty-util

install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -dm 755 $RPM_BUILD_ROOT%{confdir}
install -dm 755 $RPM_BUILD_ROOT%{homedir}
install -dm 755 $RPM_BUILD_ROOT%{logdir}
install -dm 755 $RPM_BUILD_ROOT%{rundir}
install -dm 755 $RPM_BUILD_ROOT%{tempdir}
install -dm 755 $RPM_BUILD_ROOT%{appdir}
# main pkg
unzip -q %{name}-%{version}.zip -d $RPM_BUILD_ROOT%{homedir}
mv $RPM_BUILD_ROOT%{homedir}/%{name}-%{version}/* $RPM_BUILD_ROOT%{homedir}/
rm -fr $RPM_BUILD_ROOT%{homedir}/%{name}-%{version}

chmod +x $RPM_BUILD_ROOT%{homedir}/bin/jetty-xinetd.sh
chmod +x djetty
mv djetty $RPM_BUILD_ROOT%{_bindir}/djetty
ln -s %{homedir}/bin/jetty.sh $RPM_BUILD_ROOT%{_bindir}/%{name}
install -pm 755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -pm 755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
echo '# Placeholder configuration file.  No default is provided.' > $RPM_BUILD_ROOT%{confdir}/jetty.conf
ln -s %{homedir}/lib/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-%{version}.jar
ln -s %{homedir}/lib/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}.jar
ln -s %{homedir}/lib/%{name}-util-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-util-%{version}.jar
ln -s %{homedir}/lib/%{name}-util-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-util.jar
( cat << EO_RC
JAVA_HOME=/usr/lib/jvm/java
JAVA_OPTIONS=
JETTY_HOME=%{homedir}
JETTY_CONSOLE=%{logdir}/jetty-console.log
JETTY_PORT=8080
JETTY_RUN=%{_localstatedir}/run/%{name}
JETTY_PID=\$JETTY_RUN/jetty.pid
EO_RC
) > $RPM_BUILD_ROOT%{homedir}/.jettyrc

# javadoc
mv $RPM_BUILD_ROOT%{homedir}/jxr/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

rm -fr $RPM_BUILD_ROOT%{homedir}/logs
ln -s %{logdir} $RPM_BUILD_ROOT%{homedir}/logs

mv $RPM_BUILD_ROOT%{homedir}/etc/* $RPM_BUILD_ROOT/%{confdir}
rm -fr $RPM_BUILD_ROOT%{homedir}/etc
ln -s %{confdir} $RPM_BUILD_ROOT%{homedir}/etc

mv $RPM_BUILD_ROOT%{homedir}/webapps/* $RPM_BUILD_ROOT/%{appdir}
rm -fr $RPM_BUILD_ROOT%{homedir}/webapps
ln -s %{appdir} $RPM_BUILD_ROOT%{homedir}/webapps

rm -fr $RPM_BUILD_ROOT%{homedir}/contrib
rm -fr $RPM_BUILD_ROOT%{homedir}/distribution
rm -fr $RPM_BUILD_ROOT%{homedir}/examples
rm -fr $RPM_BUILD_ROOT%{homedir}/extras
rm -fr $RPM_BUILD_ROOT%{homedir}/modules
rm -fr $RPM_BUILD_ROOT%{homedir}/patches
rm -fr $RPM_BUILD_ROOT%{homedir}/jxr
rm -fr $RPM_BUILD_ROOT%{homedir}/project-website
rm -fr $RPM_BUILD_ROOT%{homedir}/LICENSES
rm -fr $RPM_BUILD_ROOT%{homedir}/bin/jetty-service.conf
rm -fr $RPM_BUILD_ROOT%{homedir}/bin/Jetty-Service.exe
rm -fr $RPM_BUILD_ROOT%{homedir}/bin/README.jetty-cygwin.txt.txt
rm -fr $RPM_BUILD_ROOT%{homedir}/bin/build_release_bundles.sh
rm -fr $RPM_BUILD_ROOT%{homedir}/bin/jetty-cygwin.sh
rm -fr $RPM_BUILD_ROOT%{homedir}/*.txt
rm -fr $RPM_BUILD_ROOT%{homedir}/pom.*
rm -fr $RPM_BUILD_ROOT%{homedir}/*.zip

#use system jars
pushd $RPM_BUILD_ROOT%{homedir}/lib/jsp-2.0
rm -fr *.jar
build-jar-repository . ant
build-jar-repository . commons-el
build-jar-repository . tomcat6/jasper
build-jar-repository . slf4j/jcl-over-slf4j
build-jar-repository . slf4j/api
build-jar-repository . slf4j/simple
build-jar-repository . xerces-j2
build-jar-repository . xml-commons-apis
build-jar-repository . tomcat6-jsp-2.1-api
popd

pushd $RPM_BUILD_ROOT%{homedir}/lib/management/mx4j
rm -fr *.jar
build-jar-repository . mx4j/mx4j
build-jar-repository . mx4j/mx4j-tools
popd

pushd $RPM_BUILD_ROOT%{homedir}/lib/naming
build-jar-repository . javamail
rm -fr mail-*.jar
popd

pushd $RPM_BUILD_ROOT%{homedir}/lib
build-jar-repository . tomcat6-servlet-2.5-api
rm -fr servlet-api-*.jar
popd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "jetty" user and group
groupadd -r %username &>/dev/null || :
# Use /bin/sh so init script will start properly.
useradd  -r -s /bin/sh -d %homedir -M          \
                    -g %username %username &>/dev/null || :

%post
[ -x /sbin/chkconfig ] && /sbin/chkconfig --add %{name}
%update_maven_depmap

%postun
userdel  %username &>/dev/null || :
groupdel %username &>/dev/null || :
%update_maven_depmap


%preun
if [ $1 = 0 ]; then
    [ -f /var/lock/subsys/%{name} ] && %{_initrddir}/%{name} stop
    [ -f %{_initrddir}/%{name} -a -x /sbin/chkconfig ] && /sbin/chkconfig --del %{name}

    %{_sbindir}/userdel %{name} >> /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}.jar
%{_javadir}/%{name}/%{name}-%{version}.jar
%{_javadir}/%{name}/%{name}-util.jar
%{_javadir}/%{name}/%{name}-util-%{version}.jar
%{_datadir}/maven2
%{_mavendepmapfragdir}
%config(noreplace) %{confdir}
%dir %{jettylibdir}
%dir %{jettycachedir}
%{homedir}
%{appdir}
%attr(755, jetty, jetty) %{logdir}
%attr(755, jetty, jetty) %{tempdir}
%attr(755, jetty, jetty) %{rundir}
%dir %{appdir}
%doc NOTICE.txt
%doc README.txt
%doc VERSION.txt
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}

