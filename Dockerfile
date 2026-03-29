FROM iproyal/pawns-cli:latest

# إعداد المتغيرات الأساسية للتشغيل
# سيتم تعويض هذه القيم من إعدادات ريلواي (Variables)
ENTRYPOINT ["/pawns-cli"]
CMD ["-email=tahanmare0@gmail.com", "-password=FirstNameAhmed1*", "-device-id=railway-node-01", "-device-name=railway-server", "-accept-tos"]
