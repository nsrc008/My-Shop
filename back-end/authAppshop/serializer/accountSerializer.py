from authAppshop.models.account import  Account
from authAppshop.models.user    import  User
from rest_framework             import  serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['balance', 'lastChangeDate', 'isActive']

    def to_representation(self, obj):
        account = Account.objects.get(id=obj.id)
        user    = User.objects.get(id=account.user_id)
        return {
            'id'            :   account.id,
            'balance'       :   account.balance,
            'lastChangeDate':   account.lastChangeDate,
            'isActive'      :   account.isActive,
            'user'          : {
                'id'    :   user.id,
                'name'  :   user.name
            } 
        }