# This is RPM spec file:

%define _topdir %(echo $PWD)/RPM

Summary:       Afanasy server
License:       GPL
Name:          afanasy-server
Version:       @VERSION@
Release:       @RELEASE@
Group:         Applications/Graphics

Requires:      afanasy-common = @VERSION@

%description
Afanasy server init sctipts. Create user "render" if does not exists.

%prep

%build

%install

%files

%clean

%pre
echo "Afanasy server PRE INSTALL"
if [ -e /etc/init.d/afserver ]; then
   echo "Trying to stop previously installed service..."
   /etc/init.d/afserver stop || true
fi
exit 0

%post
echo "Afanasy server POST INSTALL"
id render || useradd render --create-home
/opt/cgru/afanasy/init/initlinks.sh c add afserver || true
/etc/init.d/afserver start || true
exit 0

%preun
echo "Afanasy server PRE REMOVE: $1"
[ "$1" != "0" ] && exit 0
/etc/init.d/afserver stop || true
/opt/cgru/afanasy/init/initlinks.sh c rm afserver || true
exit 0
