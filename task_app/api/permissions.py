from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsReviewerOrAssigneeOrAdmin(BasePermission):
    """
    Custom permission to only allow board Superuser, Owner and Member.
    
    Users are granted access if they are either:
    - Superuser =   SAFE_METHODS, PATCH, DELETE
    - Owner     =   SAFE_METHODS, PATCH, DELETE
    - Member    =   SAFE_METHODS, PATCH
        
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and (request.user.is_superuser or request.user == obj.reviewer_id or request.user == obj.assignee_id))
        elif request.method == 'PATCH':
            return bool(request.user and (request.user.is_superuser or request.user == obj.reviewer_id or request.user == obj.assignee_id))
        elif request.method == 'DELETE':
            return bool(request.user and (request.user.is_superuser or request.user == obj.reviewer_id))
