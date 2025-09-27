from aiogram import types

def is_admin(obj):
    if (type(obj) == types.chat_member_owner.ChatMemberOwner) or (type(obj) == types.chat_member_administrator.ChatMemberAdministrator and obj.can_restrict_members == True):
        return True
    else: return False