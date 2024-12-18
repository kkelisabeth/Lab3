# Use the official Debian base image
FROM debian:bullseye-slim

# Update package list and install OpenSSH and SNMP
RUN apt-get update && \
    apt-get install -y openssh-server snmp snmpd && \
    apt-get clean

# Configure OpenSSH to allow username enumeration
RUN echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "UsePAM no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers root" >> /etc/ssh/sshd_config && \
    service ssh restart

# Configure SNMP with default public community string
RUN echo "rocommunity public" >> /etc/snmp/snmpd.conf && \
    echo "rocommunity6 public" >> /etc/snmp/snmpd.conf && \
    service snmpd restart

# Expose SSH (22) and SNMP (161/UDP) ports
EXPOSE 22 161/udp

# Start SSH and SNMP services
CMD service ssh start && service snmpd start && tail -f /dev/null
