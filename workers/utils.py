from aiogram import types

def is_admin(obj):
    if (type(obj) == types.chat_member_owner.ChatMemberOwner) or (type(obj) == types.chat_member_administrator.ChatMemberAdministrator and obj.can_restrict_members == True):
        return True
    else: return False

def bot_is_admin(obj):
    if (type(obj) == types.chat_member_member.ChatMemberMember) or (type(obj) == types.chat_member_restricted.ChatMemberRestricted) or (types.chat_member_administrator.ChatMemberAdministrator and (obj.can_restrict_members == False or obj.can_delete_messages == False)):
        return False
    else: return True